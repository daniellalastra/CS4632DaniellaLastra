class WaitingQueue:
    def __init__(self):
        self.queues = {1: [], 2: [], 3: [], 4: [], 5: []}  # Priority levels 1-5

    def add_patient(self, patient):
        self.queues[patient.triage_level].append(patient)
        print(f"Patient {patient.patient_id} added to queue level {patient.triage_level}")

    def get_next_patient(self):
        # Check queues from highest priority (1) to lowest (5)
        for level in range(1, 6):
            if self.queues[level]:
                patient = self.queues[level].pop(0)
                print(f"Patient {patient.patient_id} retrieved from queue level {level}")
                return patient
        return None