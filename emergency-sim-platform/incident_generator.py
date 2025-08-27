from incident_data import *
import uuid
from datetime import datetime, timedelta

class Incident:
    """represents a single emergency incident"""

    def __init__(self):
        self.incident_id = str(uuid.uuid4())[:8] # short unique id
        self.timestamp = datetime.now() # timestamp of incident
        self.caller_info = self._generate_caller_info() # caller info
        self.location = self._generate_location() # location of incident
        self.emergency_type = self._generate_emergency_type() # type of emergency
        self.priority = self._generate_priority() # priority of incident
        self.operator_notes = self._generate_operator_notes() # operator notes
        self.symptoms = self._generate_symptoms() # symptoms
        self.vital_signs = self._generate_vital_signs() # vital signs
        self.patient_condition = self._generate_patient_condition() # patient condition


    def _generate_caller_info(self):
        """generate caller info"""
        return {
            "name": fake.name(),
            "age": fake.random_int(min=18, max=95),
            "sex": random.choice(["Male", "Female"]),
            "phone": fake.phone_number(),
            "medical_history": random.choice(MEDICAL_CONDITIONS)
        }

    def _generate_location(self):
        """generate location"""
        return {
            "address": generate_richmond_address(),
            "coordinates": {"latitude": 37.5407, "longitude": -77.4348}
        }

    def _generate_emergency_type(self):
        """generate emergency type"""
        all_incidents = MEDICAL_EMERGENCIES + NON_MEDICAL_EMERGENCIES
        return random.choice(all_incidents)

    def _generate_priority(self):
        """generate realistic priority level based on multiple factors"""
        base_priority = 3 # default priority

        # Factor 1: Emergency type priority
        if self.emergency_type in ["Cardiac arrest", "DOA", "Unconscious/unresponsive"]:
            base_priority = 1
        elif self.emergency_type in ["Heart attack symptoms", "Stroke symptoms", "Severe bleeding", "Respiratory arrest"]:
            base_priority = 1
        elif self.emergency_type in ["Diabetic emergency", "Seizure emergency", "Mental health crisis"]:
            base_priority = 2
        elif "Car accident" in self.emergency_type:
            base_priority = 2 if "with injuries" in self.emergency_type else 3
        elif self.emergency_type in ["Sports injury", "Fall (elderly)", "Pediatric emergency"]:
            base_priority = 2
        elif self.emergency_type in ["Non-emergency transport", "Information request"]:
            base_priority = 4

        # Factor 2: Patient age adjustments
        age = self.caller_info["age"]
        if age < 18 or age > 65: # pediatric or elderly
            if base_priority > 2:
                base_priority -= 1 # increase priority
        
        # Factor 3: time of day considerations
        hour = self.timestamp.hour
        if hour in [22, 23, 0, 1, 2, 3, 4, 5]: # late night/early morning
            if self.emergency_type in ["Mental Health Crisis", "Overdose/Poisoning"]:
                base_priority = min(base_priority, 2) # higher priority at night

        # Factor 4: Medical history considerations
        if self.caller_info['medical_history'] in ["Heart Disease", "Diabetes Type 1", "Epilepsy"]:
            if base_priority > 2:
                base_priority -= 1 # increase priority for patients with severe medical conditions

        return max(1, min(5, base_priority)) # ensure priority is between 1 and 5
        
   
    def _generate_symptoms(self):
        """generate realistic symptoms based on emergency type"""
        symptoms_map = {
           "Cardiac arrest": ["Unconscious", "No pulse", "Not breathing"],
            "Heart attack symptoms": ["Chest pain", "Shortness of breath", "Sweating", "Nausea"],
            "Stroke symptoms": ["Facial drooping", "Arm weakness", "Speech difficulty", "Confusion"],
            "Diabetic emergency": ["Confusion", "Sweating", "Shaking", "Dizziness"],
            "Seizure emergency": ["Unconscious", "Convulsions", "Foaming at mouth"],
            "Respiratory distress": ["Difficulty breathing", "Wheezing", "Chest tightness"],
            "Severe bleeding": ["Visible bleeding", "Pale skin", "Dizziness", "Weakness"],
            "Sports injury": ["Pain", "Swelling", "Limited mobility", "Bruising"],
            "Car accident with injuries": ["Pain", "Bleeding", "Neck/back pain", "Confusion"],
            "Mental health crisis": ["Agitation", "Confusion", "Suicidal thoughts", "Paranoia"] 
        }

        return symptoms_map.get(self.emergency_type, ["General distress", "Pain"])

    def _generate_vital_signs(self):
        """generate realistic vital signs based on emergency type and age"""
        age = self.caller_info["age"]

        # Base vital signs by age
        if age < 18: # pediatric
            bp_systolic = random.randint(90, 140)
            bp_diastolic = random.randint(60, 90)
            heart_rate = random.randint(70, 120)
            temp = round(random.uniform(97.0, 99.5), 1)
        elif age > 65: # elderly
            bp_systolic = random.randint(110, 180)
            bp_diastolic = random.randint(70, 100)
            heart_rate = random.randint(60, 100)
            temp = round(random.uniform(96.8, 99.2), 1)
        else: #adult
            bp_systolic = random.randint(100, 160)
            bp_diastolic = random.randint(65, 95)
            heart_rate = random.randint(60, 110)
            temp = round(random.uniform(97.2, 99.8), 1)

        # adjust based on emergency type
        if self.emergency_type in ["Cardiac arrest", "Heart attack symptoms"]:
            heart_rate = random.randint(40, 200) # irregular
            bp_systolic = random.randint(70, 200) # unstable
        elif self.emergency_type in ["Respiratory distress", "Severe bleeding"]:
            heart_rate += random.randint(20, 40) # elevated
            bp_systolic += random.randint(10, 30) # lowered

        return {
            "blood_pressure": f"{bp_systolic}/{bp_diastolic}",
            "heart_rate": heart_rate,
            "temperature": temp,
            "oxygen_saturation": random.randint(85, 100)
        }

    def _generate_patient_condition(self):
        """Generate patient condition details"""
        conditions = ["Alert and oriented", "Confused", "Drowsy", "Unconscious", "Agitated"]
        pain_levels = ["No pain", "Mild pain", "Moderate pain", "Severe pain", "Excrutiating pain"]

        # adjust based on emergency type
        if self.emergency_type in ["Cardiac arrest", "DOA"]:
            condition = "Unconscious"
            pain = "No pain"
        elif self.emergency_type in ["Severe bleeding", "Trauma"]:
            condition = random.choice(["ALert and oriented", "Confused", "Drowsy"])
            pain = random.choice(["Moderate pain", "Severe pain", "Excrutiating pain"])
        else:
            condition = random.choice(conditions)
            pain = random.choice(pain_levels)

        return {
            "mental_status": condition,
            "pain_level": pain,
            "conscious": condition != "Unconscious"
        }

    def _generate_operator_notes(self):
        """Generate more detailed operator notes"""
        symptoms = self._generate_symptoms()
        vital_signs = self._generate_vital_signs()
        condition = self._generate_patient_condition()
        
        notes = f"Caller reports {self.emergency_type.lower()}. "
        notes += f"Patient is {condition['mental_status'].lower()}. "
        notes += f"Main symptoms: {', '.join(symptoms[:2])}. "
        notes += f"BP: {vital_signs['blood_pressure']}, HR: {vital_signs['heart_rate']}. "
        notes += f"Pain level: {condition['pain_level'].lower()}."
        
        return notes

class IncidentBatchGenerator:
    """Generate a batch of incidents for testing and simulation"""

    def __init__(self):
        self.incidents = []

    def generate_batch(self, count=10):
        """Generate a batch of incidents"""
        print(f"=== GENERATING {count} INCIDENTS ===")

        for i in range(count):
            incident = Incident()
            self.incidents.append(incident)
            
            # print summary for each incident
            print(f"\n=== INCIDENT {i+1} ===")
            print(f" ID: {incident.incident_id}")
            print(f" Type: {incident.emergency_type}")
            print(f" Priority: {incident.priority}")
            print(f" Caller: {incident.caller_info['name']} ({incident.caller_info['age']} years old)")
            print(f" Location: {incident.location['address']}")
            print(f" Status: {incident.patient_condition['mental_status']}")

        return self.incidents

    def get_statistics(self):
        """Get statistics about the incidents"""
        if not self.incidents:
            return "No incidents generated yet"

        total = len(self.incidents)
        priority_counts = {}
        emergency_types = {}

        for incident in self.incidents:
            # count by priority
            priority = incident.priority
            priority_counts[priority] = priority_counts.get(priority, 0) + 1

            # count by emergency type
            emergency_type = incident.emergency_type
            emergency_types[emergency_type] = emergency_types.get(emergency_type, 0) + 1

        print(f"\n=== INCIDENT STATISTICS ===")
        print(f"Total incidents: {total}")
        print("\nPriority distribution:")
        for priority in sorted(priority_counts.keys()):
            count = priority_counts[priority]
            percentage = (count / total) * 100
            print(f" Priority {priority}: {count} ({percentage:.1f}%)")

        print(f"\nEmergency type distribution:")
        for emergency_type, count in emergency_types.items():
            percentage = (count / total) * 100
            print(f" {emergency_type}: {count} incidents ({percentage:.1f}%)")

        return {
            "total": total,
            "priority_counts": priority_counts,
            "emergency_types": emergency_types
        }



# Test the class
def test_incident_generation():
    print("=== TESTING INCIDENT GENERATION ===")
    incident = Incident()
    print(f"Incident ID: {incident.incident_id}")
    print(f"Timestamp: {incident.timestamp}")
    print(f"Caller: {incident.caller_info['name']} ({incident.caller_info['age']} years old)")
    print(f"Location: {incident.location['address']}")
    print(f"Emergency: {incident.emergency_type}")
    print(f"Priority: {incident.priority}")
    print(f"Notes: {incident.operator_notes}")

def test_batch_generation():
    print("=== TESTING BATCH GENERATION ===")
    generator = IncidentBatchGenerator()
    incidents = generator.generate_batch(5)
    stats = generator.get_statistics()
    return incidents

if __name__ == "__main__":
    test_incident_generation()
    test_batch_generation()