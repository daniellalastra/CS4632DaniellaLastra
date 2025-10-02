import simpy
import random
from patient import Patient
from resources import WaitingQueue

class EmergencyDepartmentSimulation:
    def __init__(self):
        self.env = simpy.Environment()
        self.triage_nurses = simpy.Resource(self.env, capacity=2)
        self.doctors = simpy.Resource(self.env, capacity=3)
        self.waiting_queue = WaitingQueue()
        self.patients_processed = 0
        self.data = []
        self.patient_id_counter = 0

    def patient_arrival(self):
        """Generate patient arrivals using Poisson process"""
        while True:
            # Exponential inter-arrival time (mean = 10 minutes)
            inter_arrival_time = random.expovariate(1.0/10)
            yield self.env.timeout(inter_arrival_time)

            patient = Patient(self.patient_id_counter, self.env.now)
            self.patient_id_counter += 1
            print(f"Time {self.env.now:6.1f}: Patient {patient.patient_id} arrived")
            self.env.process(self.patient_flow(patient))

    def patient_flow(self, patient):
        """Complete patient flow through the ED"""
        arrival_time = self.env.now

        # Triage process
        print(f"Time {self.env.now:6.1f}: Patient {patient.patient_id} waiting for triage")
        with self.triage_nurses.request() as request:
            yield request
            print(f"Time {self.env.now:6.1f}: Patient {patient.patient_id} started triage")
            triage_time = random.expovariate(1.0/5)  # Mean triage time = 5 min
            yield self.env.timeout(triage_time)
            patient.triage_level = random.randint(1, 5)
            print(f"Time {self.env.now:6.1f}: Patient {patient.patient_id} completed triage (Level {patient.triage_level})")

        # Add to waiting queue
        self.waiting_queue.add_patient(patient)

        # Wait for doctor
        print(f"Time {self.env.now:6.1f}: Patient {patient.patient_id} waiting for doctor")
        with self.doctors.request() as request:
            yield request
            print(f"Time {self.env.now:6.1f}: Patient {patient.patient_id} started treatment")
            treatment_time = random.expovariate(1.0/15)  # Mean treatment = 15 min
            yield self.env.timeout(treatment_time)
            print(f"Time {self.env.now:6.1f}: Patient {patient.patient_id} completed treatment")

        # Record data
        departure_time = self.env.now
        total_time = departure_time - arrival_time
        self.data.append({
            'patient_id': patient.patient_id,
            'triage_level': patient.triage_level,
            'arrival_time': arrival_time,
            'departure_time': departure_time,
            'total_time': total_time
        })
        self.patients_processed += 1

    def run(self, simulation_time=120):  # 2-hour simulation for testing
        print("=== EMERGENCY DEPARTMENT SIMULATION STARTED ===")
        print("Configuration: 2 triage nurses, 3 doctors")
        print(f"Simulation time: {simulation_time} minutes")
        print("=" * 50)

        self.env.process(self.patient_arrival())
        self.env.run(until=simulation_time)

        print("=" * 50)
        print("=== SIMULATION COMPLETED ===")
        print(f"Total patients processed: {self.patients_processed}")
        if self.data:
            avg_time = sum(d['total_time'] for d in self.data) / len(self.data)
            print(f"Average time in system: {avg_time:.2f} minutes")

            # Print patient summary
            print("\nPatient Summary:")
            for patient_data in self.data:
                print(f"Patient {patient_data['patient_id']}: Level {patient_data['triage_level']}, "
                      f"Time in system: {patient_data['total_time']:.1f} min")
        else:
            print("No patients were processed")

if __name__ == "__main__":
    sim = EmergencyDepartmentSimulation()
    sim.run()