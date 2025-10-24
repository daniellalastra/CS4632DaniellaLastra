import json
import pandas as pd
from datetime import datetime

class SimulationRunManager:
    def __init__(self, base_config):
        self.base_config = base_config
        self.all_metrics = []
        self.run_configs = []

    def generate_run_configurations(self):
        """Generate 10 different configuration sets for testing"""
        base_params = {
            'simulation_time': 480,  # 8 hours
            'num_triage_nurses': 2,
            'num_doctors': 3,
            'arrival_rate': 0.1,  # 6 patients per hour
            'triage_rate': 0.2,   # 5 minutes per triage
            'treatment_rate': 0.067,  # 15 minutes per treatment
            'random_seed': 42,
            'data_collection_interval': 5,
            'output_directory': 'simulation_runs_m3'
        }

        # Define 10 different scenarios
        self.run_configs = [
            {**base_params, 'run_id': 1, 'purpose': 'Baseline'},
            {**base_params, 'run_id': 2, 'arrival_rate': 0.15, 'purpose': 'High Arrival Rate'},
            {**base_params, 'run_id': 3, 'arrival_rate': 0.05, 'purpose': 'Low Arrival Rate'},
            {**base_params, 'run_id': 4, 'num_doctors': 2, 'purpose': 'Fewer Doctors'},
            {**base_params, 'run_id': 5, 'num_doctors': 5, 'purpose': 'More Doctors'},
            {**base_params, 'run_id': 6, 'num_triage_nurses': 1, 'purpose': 'Fewer Triage Nurses'},
            {**base_params, 'run_id': 7, 'num_triage_nurses': 4, 'purpose': 'More Triage Nurses'},
            {**base_params, 'run_id': 8, 'treatment_rate': 0.1, 'purpose': 'Faster Treatment'},
            {**base_params, 'run_id': 9, 'treatment_rate': 0.05, 'purpose': 'Slower Treatment'},
            {**base_params, 'run_id': 10, 'arrival_rate': 0.12, 'num_doctors': 4, 'purpose': 'Combined Improvement'}
        ]

        return self.run_configs

    def execute_all_runs(self):
        """Execute all simulation runs"""
        print("Starting all simulation runs...")
        print("=" * 60)

        for config in self.run_configs:
            from hospital_simulation.enhanced_simulation import EnhancedEmergencyDepartmentSimulation
            simulation = EnhancedEmergencyDepartmentSimulation(config)
            metrics = simulation.run(config['run_id'])

            # Add run information to metrics
            metrics['purpose'] = config['purpose']
            metrics['arrival_rate'] = config['arrival_rate']
            metrics['num_doctors'] = config['num_doctors']
            metrics['num_triage_nurses'] = config['num_triage_nurses']
            metrics['treatment_rate'] = config['treatment_rate']

            self.all_metrics.append(metrics)

            print(f"Completed: {config['purpose']}")
            print(f"  Patients: {metrics['total_patients']}, Avg Time: {metrics['avg_total_time']:.1f} min")
            if 'avg_doctor_utilization' in metrics:
                print(f"  Doctor Utilization: {metrics['avg_doctor_utilization']:.1%}")
            print("-" * 40)

        # Export summary of all runs
        self.export_summary()

    def export_summary(self):
        """Export summary of all runs"""
        summary_df = pd.DataFrame(self.all_metrics)

        # Reorder columns for better readability
        columns_order = ['run_id', 'purpose', 'total_patients', 'avg_total_time',
                         'avg_doctor_utilization', 'throughput', 'arrival_rate',
                         'num_doctors', 'num_triage_nurses', 'treatment_rate',
                         'real_world_duration']

        # Only include columns that exist
        available_columns = [col for col in columns_order if col in summary_df.columns]
        summary_df = summary_df[available_columns]

        # Export to CSV
        summary_df.to_csv('simulation_runs_m3/all_runs_summary.csv', index=False)

        # Print summary table
        print("\n" + "=" * 60)
        print("SIMULATION RUNS SUMMARY")
        print("=" * 60)
        print(summary_df.to_string(index=False))

        return summary_df

def main():
    # Base configuration
    base_config = {
        'output_directory': 'simulation_runs_m3'
    }

    # Create and run manager
    manager = SimulationRunManager(base_config)
    manager.generate_run_configurations()
    summary = manager.execute_all_runs()

    print(f"\nAll runs completed. Data exported to 'simulation_runs_m3/'")
    print(f"Total runs executed: {len(manager.all_metrics)}")

if __name__ == "__main__":
    main()