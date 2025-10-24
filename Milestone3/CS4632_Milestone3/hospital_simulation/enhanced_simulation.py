import simpy
import random
import json
import pandas as pd
import numpy as np
from datetime import datetime
import os
from pathlib import Path

class EnhancedEmergencyDepartmentSimulation:
    def __init__(self, config):
        self.config = config
        self.env = simpy.Environment()

        # Set default values for missing config options
        self.config.setdefault('data_collection_interval', 5)
        self.config.setdefault('random_seed', 42)

        # Resources
        self.triage_nurses = simpy.Resource(self.env, capacity=config['num_triage_nurses'])
        self.doctors = simpy.Resource(self.env, capacity=config['num_doctors'])

        # Tracking systems
        self.waiting_queue = None
        self.patient_id_counter = 0
        self.run_data = {
            'patients': [],
            'resource_utilization': [],
            'system_metrics': {},
            'queue_metrics': {}
        }

        # Set random seed for reproducibility
        random.seed(config.get('random_seed', 42))
        np.random.seed(config.get('random_seed', 42))

        # Create output directory
        self.output_dir = Path(config.get('output_directory', 'simulation_runs'))
        self.output_dir.mkdir(exist_ok=True)

    def patient_arrival_process(self):
        """Generate patient arrivals using Poisson process"""
        while True:
            inter_arrival_time = random.expovariate(self.config['arrival_rate'])
            yield self.env.timeout(inter_arrival_time)

            # Import Patient here to avoid circular imports
            from hospital_simulation.patient import Patient
            patient = Patient(self.patient_id_counter, self.env.now)
            patient.assign_triage_level()
            self.patient_id_counter += 1

            # Record arrival
            self.record_event('ARRIVAL', patient)
            self.env.process(self.patient_flow(patient))

    def patient_flow(self, patient):
        """Complete patient flow through the ED"""
        # Triage process
        patient.triage_start_time = self.env.now
        with self.triage_nurses.request() as request:
            yield request
            patient.triage_start_time = self.env.now
            self.record_event('TRIAGE_START', patient)

            triage_time = random.expovariate(self.config['triage_rate'])
            yield self.env.timeout(triage_time)

            patient.triage_end_time = self.env.now
            self.record_event('TRIAGE_END', patient)

        # Wait for doctor in priority queue
        if self.waiting_queue is None:
            from hospital_simulation.waiting_queue import WaitingQueue
            self.waiting_queue = WaitingQueue()

        self.waiting_queue.add_patient(patient, self.env.now)
        self.record_event('QUEUED_FOR_TREATMENT', patient)

        # Wait for doctor (this is the fixed part)
        with self.doctors.request() as request:
            yield request

            # Get the next patient from the queue (should be this patient due to priority)
            next_patient = self.waiting_queue.get_next_patient(self.env.now)

            patient.treatment_start_time = self.env.now
            self.record_event('TREATMENT_START', patient)

            treatment_time = random.expovariate(self.config['treatment_rate'])
            yield self.env.timeout(treatment_time)

            patient.treatment_end_time = self.env.now
            self.record_event('TREATMENT_END', patient)

        # Record complete patient journey
        self.record_patient_completion(patient)

    def resource_monitor(self):
        """Monitor resource utilization at regular intervals"""
        while True:
            # Record current resource states
            utilization_data = {
                'time': self.env.now,
                'triage_nurses_busy': self.triage_nurses.count,
                'triage_nurses_available': self.triage_nurses.capacity - self.triage_nurses.count,
                'doctors_busy': self.doctors.count,
                'doctors_available': self.doctors.capacity - self.doctors.count,
                'triage_utilization': self.triage_nurses.count / self.triage_nurses.capacity,
                'doctor_utilization': self.doctors.count / self.doctors.capacity
            }
            self.run_data['resource_utilization'].append(utilization_data)

            yield self.env.timeout(self.config.get('data_collection_interval', 5))

    def record_event(self, event_type, patient):
        """Record significant events"""
        # This method records events - you can expand it to store events if needed
        pass

    def record_patient_completion(self, patient):
        """Record complete patient data when they exit system"""
        wait_times = patient.calculate_wait_times()

        patient_data = {
            'patient_id': patient.patient_id,
            'triage_level': patient.triage_level,
            'arrival_time': patient.arrival_time,
            'triage_start_time': patient.triage_start_time,
            'triage_end_time': patient.triage_end_time,
            'treatment_start_time': patient.treatment_start_time,
            'treatment_end_time': patient.treatment_end_time,
            'wait_for_triage': wait_times['wait_for_triage'],
            'triage_duration': wait_times['triage_duration'],
            'wait_for_treatment': wait_times['wait_for_treatment'],
            'treatment_duration': wait_times['treatment_duration'],
            'total_time_in_system': wait_times['total_time']
        }

        self.run_data['patients'].append(patient_data)

    def calculate_system_metrics(self):
        """Calculate overall system performance metrics"""
        if not self.run_data['patients']:
            return {}

        df_patients = pd.DataFrame(self.run_data['patients'])

        metrics = {
            'total_patients_processed': len(df_patients),
            'simulation_duration': self.env.now,
            'throughput': len(df_patients) / self.env.now,

            # Patient time metrics
            'avg_total_time': df_patients['total_time_in_system'].mean(),
            'avg_wait_for_triage': df_patients['wait_for_triage'].mean(),
            'avg_wait_for_treatment': df_patients['wait_for_treatment'].mean(),

            # Service time metrics
            'avg_triage_time': df_patients['triage_duration'].mean(),
            'avg_treatment_time': df_patients['treatment_duration'].mean(),
        }

        # Add resource utilization if we have that data
        if self.run_data['resource_utilization']:
            df_resources = pd.DataFrame(self.run_data['resource_utilization'])
            metrics.update({
                'avg_triage_utilization': df_resources['triage_utilization'].mean(),
                'avg_doctor_utilization': df_resources['doctor_utilization'].mean(),
                'max_triage_utilization': df_resources['triage_utilization'].max(),
                'max_doctor_utilization': df_resources['doctor_utilization'].max(),
            })

        # By triage level
        metrics['metrics_by_triage_level'] = {}
        for level in range(1, 6):
            level_data = df_patients[df_patients['triage_level'] == level]
            if len(level_data) > 0:
                metrics['metrics_by_triage_level'][level] = {
                    'count': len(level_data),
                    'avg_total_time': level_data['total_time_in_system'].mean(),
                    'avg_wait_for_treatment': level_data['wait_for_treatment'].mean(),
                    'max_wait_for_treatment': level_data['wait_for_treatment'].max()
                }

        return metrics

    def export_data(self, run_id):
        """Export all collected data to files"""
        run_dir = self.output_dir / f"run_{run_id:03d}"
        run_dir.mkdir(exist_ok=True)

        # Export patient data
        if self.run_data['patients']:
            df_patients = pd.DataFrame(self.run_data['patients'])
            df_patients.to_csv(run_dir / "patients.csv", index=False)

        # Export resource utilization data
        if self.run_data['resource_utilization']:
            df_resources = pd.DataFrame(self.run_data['resource_utilization'])
            df_resources.to_csv(run_dir / "resource_utilization.csv", index=False)

        # Export queue data if we have it
        if self.waiting_queue:
            try:
                self.waiting_queue.export_queue_data(run_dir / "queue_history.csv")
            except:
                pass  # If export fails, continue anyway

        # Calculate and export system metrics
        system_metrics = self.calculate_system_metrics()

        metrics_data = {
            'run_id': run_id,
            'timestamp': datetime.now().isoformat(),
            'config': self.config,
            'system_metrics': system_metrics,
        }

        with open(run_dir / "metrics.json", 'w') as f:
            json.dump(metrics_data, f, indent=2)

        # Also export flat metrics for CSV
        metrics_flat = {
            'run_id': run_id,
            'total_patients': system_metrics.get('total_patients_processed', 0),
            'avg_total_time': system_metrics.get('avg_total_time', 0),
            'throughput': system_metrics.get('throughput', 0)
        }

        # Add utilization if available
        if 'avg_doctor_utilization' in system_metrics:
            metrics_flat['avg_doctor_utilization'] = system_metrics['avg_doctor_utilization']

        return metrics_flat

    def run(self, run_id):
        """Run the simulation"""
        print(f"Starting simulation run {run_id}")
        print(f"Configuration: {self.config}")

        # Start processes
        self.env.process(self.patient_arrival_process())
        self.env.process(self.resource_monitor())

        # Run simulation
        start_time = datetime.now()
        self.env.run(until=self.config['simulation_time'])
        end_time = datetime.now()

        # Export data
        metrics = self.export_data(run_id)
        metrics['real_world_duration'] = (end_time - start_time).total_seconds()

        print(f"Completed run {run_id}: Processed {metrics['total_patients']} patients")

        return metrics