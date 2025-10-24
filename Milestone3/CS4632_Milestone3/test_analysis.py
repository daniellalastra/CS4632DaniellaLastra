import pandas as pd
import json
from pathlib import Path

def analyze_test_results():
    """Analyze and create test results report"""

    print("=== GENERATING TEST RESULTS ===")

    try:
        # Load the summary data from your simulation runs
        summary_df = pd.read_csv('simulation_runs_m3/all_runs_summary.csv')
        print("✅ Found simulation data!")

        # Create a clean CSV file for submission
        csv_data = []
        for index, run in summary_df.iterrows():
            csv_data.append({
                'Run ID': run['run_id'],
                'Scenario': run['purpose'],
                'Total Patients': run['total_patients'],
                'Avg Time in System (min)': f"{run['avg_total_time']:.1f}",
                'Doctor Utilization (%)': f"{run['avg_doctor_utilization']:.1%}",
                'Throughput (patients/hour)': f"{run['throughput'] * 60:.2f}",
                'Real Duration (seconds)': f"{run['real_world_duration']:.1f}"
            })

        # Save as CSV file
        results_df = pd.DataFrame(csv_data)
        results_df.to_csv('test_results.csv', index=False)

        print("✅ test_results.csv created successfully!")
        print("📍 File location: /Users/dani/Desktop/CS4632Daniellalastra/Milestone3/CS4632_Milestone3/test_results.csv")

        # Show what we created
        print("\n📊 TEST RESULTS SUMMARY:")
        print(results_df.to_string(index=False))

        return results_df

    except FileNotFoundError:
        print("❌ ERROR: Could not find simulation data!")
        print("   Make sure you ran the simulations first and have:")
        print("   - simulation_runs_m3/all_runs_summary.csv")
        return None

if __name__ == "__main__":
    analyze_test_results()