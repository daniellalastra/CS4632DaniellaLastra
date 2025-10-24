from run_manager import SimulationRunManager
import json

def main():
    print("=== Hospital ED Simulation - Milestone 3 ===")

    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        print("✅ Config loaded successfully")
    except FileNotFoundError:
        print("❌ config.json not found - using defaults")
        config = {}

    manager = SimulationRunManager(config)
    manager.generate_run_configurations()
    manager.execute_all_runs()

    print("\n🎉 Simulation completed! Check 'simulation_runs_m3' folder for results")

if __name__ == "__main__":
    main()