class Patient:
    def __init__(self, patient_id, arrival_time):
        self.patient_id = patient_id
        self.arrival_time = arrival_time
        self.triage_level = None
        self.priority = None
        self.treatment_time = None

    def __str__(self):
        return f"Patient {self.patient_id} (Level {self.triage_level})"