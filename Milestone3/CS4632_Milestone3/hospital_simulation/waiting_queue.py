import pandas as pd

class WaitingQueue:
    def __init__(self):
        self.queues = {1: [], 2: [], 3: [], 4: [], 5: []}  # Priority levels 1-5
        self.queue_history = []

    def add_patient(self, patient, current_time=None):
        """Add patient to appropriate queue"""
        self.queues[patient.triage_level].append(patient)
        print(f"Patient {patient.patient_id} added to queue level {patient.triage_level}")

        # Record queue state if current_time is provided
        if current_time is not None:
            self.record_queue_state(current_time)

    def get_next_patient(self, current_time=None):
        """Get next patient based on priority"""
        for level in range(1, 6):
            if self.queues[level]:
                patient = self.queues[level].pop(0)
                print(f"Patient {patient.patient_id} retrieved from queue level {level}")

                # Record queue state if current_time is provided
                if current_time is not None:
                    self.record_queue_state(current_time)
                return patient
        return None

    def record_queue_state(self, current_time):
        """Record current state of all queues"""
        queue_state = {
            'time': current_time,
            'queue_1_length': len(self.queues[1]),
            'queue_2_length': len(self.queues[2]),
            'queue_3_length': len(self.queues[3]),
            'queue_4_length': len(self.queues[4]),
            'queue_5_length': len(self.queues[5]),
            'total_queue_length': sum(len(q) for q in self.queues.values())
        }
        self.queue_history.append(queue_state)

    def export_queue_data(self, filename):
        """Export queue history to CSV"""
        if self.queue_history:
            df = pd.DataFrame(self.queue_history)
            df.to_csv(filename, index=False)