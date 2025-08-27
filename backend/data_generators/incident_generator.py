"""
Incident Generator

Generates realistic emergency incident data including caller information,
location, emergency types, priority levels, and medical details for the
emergency services simulation.
"""

import random
from datetime import datetime, timedelta
from .base_generator import BaseGenerator
from incident_data import *


class IncidentGenerator(BaseGenerator):
    """Generates emergency incident data"""
    
    def __init__(self):
        super().__init__()
        
        # Emergency type categories
        self.medical_emergencies = MEDICAL_EMERGENCIES
        self.non_medical_emergencies = NON_MEDICAL_EMERGENCIES
        self.medical_conditions = MEDICAL_CONDITIONS
    
    def generate_incident(self):
        """Generate a single emergency incident with complete information"""
        
        incident_id = self.generate_id(prefix="INC", length=8)
        timestamp = datetime.now()
        
        # Generate all incident components
        caller_info = self._generate_caller_info()
        location = self._generate_location()
        emergency_type = self._generate_emergency_type()
        priority = self._generate_priority(emergency_type, caller_info, timestamp)
        operator_notes = self._generate_operator_notes(emergency_type, caller_info)
        symptoms = self._generate_symptoms(emergency_type)
        vital_signs = self._generate_vital_signs(emergency_type, caller_info)
        patient_condition = self._generate_patient_condition(emergency_type, vital_signs)
        
        incident = {
            'incident_id': incident_id,
            'timestamp': timestamp,
            'caller_info': caller_info,
            'location': location,
            'emergency_type': emergency_type,
            'priority': priority,
            'operator_notes': operator_notes,
            'symptoms': symptoms,
            'vital_signs': vital_signs,
            'patient_condition': patient_condition,
            'status': 'dispatched',
            'created_timestamp': datetime.now()
        }
        
        # Validate and store
        if self.validate_data(incident):
            self.add_to_generated_data(incident)
        
        return incident
    
    def _generate_caller_info(self):
        """Generate caller information"""
        age = random.randint(18, 95)
        sex = random.choice(["Male", "Female"])
        
        return {
            "name": self.fake.name(),
            "age": age,
            "sex": sex,
            "phone": self.fake.phone_number(),
            "medical_history": random.choice(self.medical_conditions)
        }
    
    def _generate_location(self):
        """Generate incident location"""
        return {
            "address": self.generate_richmond_address(),
            "coordinates": self.generate_richmond_coordinates()
        }
    
    def _generate_emergency_type(self):
        """Generate emergency type"""
        all_incidents = self.medical_emergencies + self.non_medical_emergencies
        return random.choice(all_incidents)
    
    def _generate_priority(self, emergency_type, caller_info, timestamp):
        """Generate realistic priority level based on multiple factors"""
        base_priority = 3  # default priority
        
        # Factor 1: Emergency type priority
        if emergency_type in ["Cardiac arrest", "DOA", "Unconscious/unresponsive"]:
            base_priority = 1
        elif emergency_type in ["Heart attack symptoms", "Stroke symptoms", "Severe bleeding", "Respiratory arrest"]:
            base_priority = 1
        elif emergency_type in ["Diabetic emergency", "Seizure emergency", "Mental health crisis"]:
            base_priority = 2
        elif "Car accident" in emergency_type:
            base_priority = 2 if "with injuries" in emergency_type else 3
        elif emergency_type in ["Sports injury", "Fall (elderly)", "Pediatric emergency"]:
            base_priority = 2
        elif emergency_type in ["Non-emergency transport", "Information request"]:
            base_priority = 4
        
        # Factor 2: Patient age adjustments
        age = caller_info["age"]
        if age < 18 or age > 65:  # pediatric or elderly
            if base_priority > 2:
                base_priority -= 1  # increase priority
        
        # Factor 3: Time of day considerations
        hour = timestamp.hour
        if hour in [22, 23, 0, 1, 2, 3, 4, 5]:  # late night/early morning
            if emergency_type in ["Mental Health Crisis", "Overdose/Poisoning"]:
                base_priority = min(base_priority, 2)  # higher priority at night
        
        # Factor 4: Medical history considerations
        if caller_info['medical_history'] in ["Heart Disease", "Diabetes Type 1", "Epilepsy"]:
            if base_priority > 2:
                base_priority -= 1  # increase priority for patients with severe medical conditions
        
        return max(1, min(5, base_priority))  # ensure priority is between 1 and 5
    
    def _generate_symptoms(self, emergency_type):
        """Generate realistic symptoms based on emergency type"""
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
        
        return symptoms_map.get(emergency_type, ["General distress", "Pain"])
    
    def _generate_vital_signs(self, emergency_type, caller_info):
        """Generate realistic vital signs based on emergency type and age"""
        age = caller_info["age"]
        
        # Base vital signs by age group
        if age < 18:  # Pediatric
            base_bp = random.randint(90, 120)
            base_hr = random.randint(60, 100)
            base_rr = random.randint(16, 24)
            base_temp = round(random.uniform(97.0, 99.5), 1)
        elif age > 65:  # Elderly
            base_bp = random.randint(110, 160)
            base_hr = random.randint(50, 90)
            base_rr = random.randint(14, 22)
            base_temp = round(random.uniform(96.8, 99.2), 1)
        else:  # Adult
            base_bp = random.randint(100, 140)
            base_hr = random.randint(60, 100)
            base_rr = random.randint(12, 20)
            base_temp = round(random.uniform(97.0, 99.0), 1)
        
        # Adjust based on emergency type
        if emergency_type in ["Cardiac arrest", "Heart attack symptoms"]:
            base_hr = random.randint(120, 180)
            base_bp = random.randint(80, 140)
        elif emergency_type in ["Respiratory distress", "Respiratory arrest"]:
            base_rr = random.randint(25, 40)
            base_hr = random.randint(100, 140)
        elif emergency_type in ["Severe bleeding", "Shock"]:
            base_hr = random.randint(100, 140)
            base_bp = random.randint(70, 110)
        elif emergency_type in ["Diabetic emergency"]:
            base_hr = random.randint(90, 130)
            base_bp = random.randint(90, 140)
        
        return {
            "blood_pressure": f"{base_bp}/{base_bp - random.randint(10, 30)}",
            "heart_rate": base_hr,
            "respiratory_rate": base_rr,
            "temperature": base_temp,
            "oxygen_saturation": random.randint(85, 100)
        }
    
    def _generate_patient_condition(self, emergency_type, vital_signs):
        """Generate patient condition based on emergency type and vital signs"""
        
        # Mental status based on emergency type
        mental_status_options = {
            "Cardiac arrest": ["Unresponsive", "Unconscious"],
            "Stroke symptoms": ["Confused", "Altered mental status", "Unresponsive"],
            "Diabetic emergency": ["Confused", "Altered mental status", "Unconscious"],
            "Seizure emergency": ["Post-ictal", "Confused", "Unconscious"],
            "Mental health crisis": ["Agitated", "Confused", "Alert"],
            "Car accident with injuries": ["Confused", "Alert", "Unconscious"],
            "default": ["Alert", "Confused", "Drowsy"]
        }
        
        mental_status = mental_status_options.get(emergency_type, mental_status_options["default"])
        
        # Pain level based on emergency type
        pain_levels = {
            "Cardiac arrest": 0,
            "Heart attack symptoms": random.randint(7, 10),
            "Stroke symptoms": random.randint(3, 8),
            "Sports injury": random.randint(5, 9),
            "Car accident with injuries": random.randint(6, 10),
            "Severe bleeding": random.randint(7, 10),
            "default": random.randint(1, 6)
        }
        
        pain_level = pain_levels.get(emergency_type, pain_levels["default"])
        
        return {
            "mental_status": random.choice(mental_status),
            "pain_level": pain_level,
            "consciousness": "Conscious" if pain_level > 0 else "Unconscious",
            "breathing": "Normal" if vital_signs["respiratory_rate"] < 25 else "Labored",
            "circulation": "Normal" if vital_signs["blood_pressure"].split('/')[0] > '90' else "Poor"
        }
    
    def _generate_operator_notes(self, emergency_type, caller_info):
        """Generate operator notes based on emergency type and caller info"""
        
        notes_templates = {
            "Cardiac arrest": [
                f"Caller reports {caller_info['name']} is unresponsive and not breathing. CPR instructions given.",
                f"Patient found unconscious by {caller_info['name']}. No pulse detected."
            ],
            "Heart attack symptoms": [
                f"{caller_info['name']} reports severe chest pain radiating to left arm.",
                f"Patient experiencing chest tightness and shortness of breath for {random.randint(10, 60)} minutes."
            ],
            "Stroke symptoms": [
                f"Caller noticed {caller_info['name']} has facial drooping and slurred speech.",
                f"Patient suddenly developed weakness on one side and confusion."
            ],
            "Car accident with injuries": [
                f"Vehicle collision reported. {caller_info['name']} complaining of neck and back pain.",
                f"Multi-vehicle accident. Patient trapped in vehicle with visible injuries."
            ],
            "Mental health crisis": [
                f"{caller_info['name']} expressing suicidal thoughts and is currently agitated.",
                f"Patient experiencing severe anxiety and paranoia. No weapons involved."
            ]
        }
        
        if emergency_type in notes_templates:
            return random.choice(notes_templates[emergency_type])
        else:
            return f"Caller {caller_info['name']} reports {emergency_type.lower()}. Patient alert and oriented."
    
    def generate_batch(self, count=10):
        """Generate a batch of incidents"""
        print(f"=== GENERATING {count} INCIDENTS ===")
        
        incidents = []
        for i in range(count):
            incident = self.generate_incident()
            incidents.append(incident)
            
            print(f"\n=== INCIDENT {i+1} ===")
            print(f" ID: {incident['incident_id']}")
            print(f" Type: {incident['emergency_type']}")
            print(f" Priority: {incident['priority']}")
            print(f" Caller: {incident['caller_info']['name']} ({incident['caller_info']['age']} years old)")
            print(f" Location: {incident['location']['address']}")
            print(f" Status: {incident['patient_condition']['mental_status']}")
        
        return incidents
    
    def validate_data(self, incident):
        """Validate incident data"""
        required_fields = ['incident_id', 'timestamp', 'emergency_type', 'priority', 'caller_info', 'location']
        
        for field in required_fields:
            if field not in incident or incident[field] is None:
                print(f"❌ Validation failed: Missing {field}")
                return False
        
        # Priority validation
        if incident['priority'] < 1 or incident['priority'] > 5:
            print(f"❌ Validation failed: Invalid priority {incident['priority']}")
            return False
        
        # Age validation
        if incident['caller_info']['age'] < 0 or incident['caller_info']['age'] > 120:
            print(f"❌ Validation failed: Invalid age {incident['caller_info']['age']}")
            return False
        
        return True
    
    def get_statistics(self):
        """Get statistics about generated incident data"""
        if not self.generated_data:
            return super().get_statistics()
        
        # Calculate statistics
        priority_counts = {}
        emergency_type_counts = {}
        
        for incident in self.generated_data:
            priority = incident['priority']
            emergency_type = incident['emergency_type']
            
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
            emergency_type_counts[emergency_type] = emergency_type_counts.get(emergency_type, 0) + 1
        
        return {
            'total_generated': len(self.generated_data),
            'generator_type': self.__class__.__name__,
            'priority_distribution': priority_counts,
            'emergency_type_distribution': emergency_type_counts,
            'average_priority': sum(incident['priority'] for incident in self.generated_data) / len(self.generated_data)
        }


# Test function
def test_incident_generation():
    """Test the incident generator functionality"""
    generator = IncidentGenerator()
    
    # Generate a few incidents
    incidents = generator.generate_batch(3)
    
    # Print statistics
    stats = generator.get_statistics()
    print(f"\n=== INCIDENT STATISTICS ===")
    for key, value in stats.items():
        print(f" {key}: {value}")


if __name__ == "__main__":
    test_incident_generation()