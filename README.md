# CS4632 - Emergency Department Simulation

A discrete-event simulation designed to model and optimize patient flow in a hospital emergency department. Built using queuing theory and priority-based scheduling to analyze key performance metrics.

## Features
- Priority-based patient triage simulation
- Tracks patient wait times and resource utilization
- Configurable simulation parameters via `config.json`
- Multiple test scenarios and run management
- Statistical analysis of simulation results

## Project Structure
- `main.py` - Entry point for the simulation
- `run_manager.py` - Manages simulation runs
- `config.json` - Simulation configuration settings
- `test_analysis.py` - Analyzes test results
- `hospital_simulation/` - Core simulation logic

## Milestones
- **Milestone 1** - Project proposal, literature review, and UML design diagrams
- **Milestone 2** - Initial implementation including core simulation framework, entity classes (Patient, TriageNurse, Doctor, WaitingQueue), Poisson arrival process, and priority queue structure using SimPy
- **Milestone 3** - Enhanced simulation with 10 test scenarios and statistical analysis

## Built With
- Python
- SimPy (discrete-event simulation)
- Queuing theory

## Installation
```bash
pip install -r requirements.txt
```

## Author
Daniella Lastra
