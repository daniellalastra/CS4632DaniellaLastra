# Hospital ED Triage Simulation

## Project Status (M2 - Initial Implementation)
**What's Implemented:**
- Core simulation framework using SimPy
- Entity classes: `Patient`, `TriageNurse`, `Doctor`, `WaitingQueue`
- Patient arrival process using Poisson process (exponential inter-arrival times)
- Triage level assignment and priority queue structure
- Basic patient flow through triage and treatment processes

**What's In Progress / Next:**
- Implementing priority-based treatment scheduling (non-preemptive)
- Enhancing data collection for performance metrics
- Adding configuration files for easy parameter adjustment
- Implementing visualization and analysis tools

**Changes from M1 Proposal:**
No major design changes. The implementation faithfully follows the M1 UML and system description.

## Installation & Setup
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt