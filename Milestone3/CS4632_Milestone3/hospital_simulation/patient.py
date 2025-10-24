import random
from dataclasses import dataclass
from typing import Optional

@dataclass
class Patient:
    patient_id: int
    arrival_time: float
    triage_level: Optional[int] = None
    priority: Optional[int] = None
    treatment_time: Optional[float] = None
    triage_start_time: Optional[float] = None
    triage_end_time: Optional[float] = None
    treatment_start_time: Optional[float] = None
    treatment_end_time: Optional[float] = None

    def assign_triage_level(self):
        """Assign triage level with realistic distribution"""
        # More realistic: fewer critical patients, more moderate cases
        weights = [0.05, 0.1, 0.35, 0.4, 0.1]  # Level 1-5 probabilities
        self.triage_level = random.choices([1, 2, 3, 4, 5], weights=weights)[0]
        self.priority = 6 - self.triage_level  # Higher priority for lower levels

    def calculate_wait_times(self):
        """Calculate various wait times"""
        wait_for_triage = self.triage_start_time - self.arrival_time if self.triage_start_time else 0
        triage_duration = self.triage_end_time - self.triage_start_time if self.triage_end_time else 0
        wait_for_treatment = self.treatment_start_time - self.triage_end_time if self.treatment_start_time else 0
        treatment_duration = self.treatment_end_time - self.treatment_start_time if self.treatment_end_time else 0
        total_time = self.treatment_end_time - self.arrival_time if self.treatment_end_time else 0

        return {
            'wait_for_triage': wait_for_triage,
            'triage_duration': triage_duration,
            'wait_for_treatment': wait_for_treatment,
            'treatment_duration': treatment_duration,
            'total_time': total_time
        }

    def __str__(self):
        return f"Patient {self.patient_id} (Level {self.triage_level})"