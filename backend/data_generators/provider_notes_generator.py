"""
Provider Notes Generator

Generates realistic field provider notes, updates, and medical reports
for the emergency services simulation including real-time updates and
comprehensive incident reports.
"""

import random
from datetime import datetime, timedelta
from .base_generator import BaseGenerator


class ProviderNotesGenerator(BaseGenerator):
    """Generates provider notes and field updates"""
    
    def __init__(self):
        super().__init__()
        
        # Note Types and Categories
        self.note_types = {
            "ARRIVAL": {
                "name": "Unit Arrival",
                "templates": [
                    "Unit {unit_id} arrived on scene at {time}. Scene appears {scene_condition}.",
                    "Arrived at {time}. Initial assessment beginning.",
                    "On scene at {time}. {scene_description}"
                ]
            },
            "ASSESSMENT": {
                "name": "Patient Assessment",
                "templates": [
                    "Patient {patient_condition}. Vital signs: BP {bp}, HR {hr}, RR {rr}, O2 {o2}%.",
                    "Initial assessment complete. Patient is {consciousness} and {orientation}.",
                    "Primary survey: {primary_findings}. Secondary survey: {secondary_findings}."
                ]
            },
            "TREATMENT": {
                "name": "Treatment Provided",
                "templates": [
                    "Treatment initiated: {treatments}. Patient response: {response}.",
                    "Interventions performed: {interventions}. Vital signs improving.",
                    "Medications administered: {medications}. Patient tolerating well."
                ]
            },
            "TRANSPORT": {
                "name": "Transport Decision",
                "templates": [
                    "Patient transported to {hospital} via {transport_mode}. ETA: {eta}.",
                    "Transport initiated to {hospital}. Patient stable during transport.",
                    "En route to {hospital}. Patient condition: {condition}."
                ]
            },
            "HANDOFF": {
                "name": "Hospital Handoff",
                "templates": [
                    "Patient transferred to {hospital_staff}. Handoff completed at {time}.",
                    "Report given to {staff_role}. Patient stable upon arrival.",
                    "Transfer complete. Patient admitted to {department}."
                ]
            },
            "COMPLICATION": {
                "name": "Complication/Issue",
                "templates": [
                    "Complication noted: {complication}. Additional interventions required.",
                    "Patient condition deteriorated: {deterioration}. Emergency protocols initiated.",
                    "Equipment issue: {issue}. Backup equipment utilized."
                ]
            }
        }
        
        # Medical terminology and phrases
        self.medical_terms = {
            "consciousness": ["Alert", "Verbal", "Pain", "Unresponsive"],
            "orientation": ["Oriented x3", "Oriented x2", "Oriented x1", "Disoriented"],
            "scene_condition": ["Safe", "Unsafe", "Controlled", "Chaotic", "Well-lit", "Dark"],
            "patient_condition": ["Stable", "Unstable", "Critical", "Improving", "Deteriorating"],
            "response": ["Positive", "Negative", "Partial", "No response", "Excellent"],
            "transport_mode": ["Ground ambulance", "Air medical", "ALS transport", "BLS transport"],
            "staff_role": ["ED physician", "Nurse", "Charge nurse", "Resident", "Attending"]
        }
        
        # Common treatments and interventions
        self.treatments = [
            "Oxygen therapy", "IV access", "Cardiac monitoring", "Splinting",
            "Wound care", "Medication administration", "CPR", "Defibrillation",
            "Airway management", "Pain management", "Fluid resuscitation"
        ]
        
        self.medications = [
            "Aspirin", "Nitroglycerin", "Albuterol", "Epinephrine", "Atropine",
            "Lidocaine", "Amiodarone", "Morphine", "Fentanyl", "Ketamine",
            "Midazolam", "Naloxone", "Glucagon", "D50", "Normal saline"
        ]
    
    def generate_provider_note(self, incident_id, crew_id, note_type=None, context=None):
        """Generate a single provider note with realistic medical content"""
        
        # Determine note type
        if note_type is None:
            note_type = random.choice(list(self.note_types.keys()))
        
        note_info = self.note_types[note_type]
        
        # Generate note ID and timestamp
        note_id = self.generate_id(prefix="NOTE", length=8)
        timestamp = datetime.now()
        
        # Generate note content based on type
        content = self._generate_note_content(note_type, context)
        
        # Determine priority based on note type
        priority_map = {
            "ARRIVAL": "Low",
            "ASSESSMENT": "Medium", 
            "TREATMENT": "High",
            "TRANSPORT": "Medium",
            "HANDOFF": "Low",
            "COMPLICATION": "Critical"
        }
        
        priority = priority_map.get(note_type, "Medium")
        
        # Generate additional metadata
        note = {
            'note_id': note_id,
            'incident_id': incident_id,
            'crew_id': crew_id,
            'note_type': note_type,
            'note_category': note_info['name'],
            'content': content,
            'priority': priority,
            'timestamp': timestamp,
            'is_urgent': priority in ["High", "Critical"],
            'requires_followup': note_type in ["COMPLICATION", "TREATMENT"],
            'created_timestamp': datetime.now()
        }
        
        # Validate and store
        if self.validate_data(note):
            self.add_to_generated_data(note)
        
        return note
    
    def _generate_note_content(self, note_type, context=None):
        """Generate realistic note content based on type and context"""
        
        if context is None:
            context = {}
        
        template = random.choice(self.note_types[note_type]['templates'])
        
        # Fill in template variables
        content = template
        
        # Replace time placeholders
        content = content.replace("{time}", datetime.now().strftime("%H:%M"))
        
        # Replace unit/hospital placeholders
        content = content.replace("{unit_id}", context.get('unit_id', f"Unit-{random.randint(1, 999):03d}"))
        content = content.replace("{hospital}", context.get('hospital', "VCU Medical Center"))
        content = content.replace("{hospital_staff}", context.get('staff', "ED physician"))
        content = content.replace("{staff_role}", random.choice(self.medical_terms['staff_role']))
        
        # Replace medical assessment placeholders
        content = content.replace("{patient_condition}", random.choice(self.medical_terms['patient_condition']))
        content = content.replace("{consciousness}", random.choice(self.medical_terms['consciousness']))
        content = content.replace("{orientation}", random.choice(self.medical_terms['orientation']))
        content = content.replace("{scene_condition}", random.choice(self.medical_terms['scene_condition']))
        content = content.replace("{response}", random.choice(self.medical_terms['response']))
        content = content.replace("{transport_mode}", random.choice(self.medical_terms['transport_mode']))
        
        # Replace vital signs placeholders
        content = content.replace("{bp}", f"{random.randint(80, 180)}/{random.randint(50, 100)}")
        content = content.replace("{hr}", str(random.randint(60, 140)))
        content = content.replace("{rr}", str(random.randint(12, 30)))
        content = content.replace("{o2}", str(random.randint(85, 100)))
        
        # Replace treatment placeholders
        if "{treatments}" in content:
            treatments = random.sample(self.treatments, random.randint(1, 3))
            content = content.replace("{treatments}", ", ".join(treatments))
        
        if "{interventions}" in content:
            interventions = random.sample(self.treatments, random.randint(1, 4))
            content = content.replace("{interventions}", ", ".join(interventions))
        
        if "{medications}" in content:
            medications = random.sample(self.medications, random.randint(1, 2))
            content = content.replace("{medications}", ", ".join(medications))
        
        # Replace other placeholders
        content = content.replace("{eta}", f"{random.randint(5, 25)} minutes")
        content = content.replace("{condition}", random.choice(self.medical_terms['patient_condition']))
        content = content.replace("{department}", random.choice(["ED", "ICU", "Cardiology", "Trauma"]))
        
        # Add medical context if needed
        if "{scene_description}" in content:
            scene_descriptions = [
                "Patient found in living room", "Patient in vehicle", "Patient on sidewalk",
                "Patient in workplace", "Patient at residence", "Patient in public area"
            ]
            content = content.replace("{scene_description}", random.choice(scene_descriptions))
        
        if "{primary_findings}" in content:
            primary_findings = [
                "ABCs intact", "Airway patent", "Breathing adequate", "Circulation present",
                "No obvious trauma", "Signs of trauma present", "Neurological deficit noted"
            ]
            content = content.replace("{primary_findings}", random.choice(primary_findings))
        
        if "{secondary_findings}" in content:
            secondary_findings = [
                "No additional injuries", "Minor abrasions noted", "Swelling present",
                "Deformity noted", "Bleeding controlled", "Pain on palpation"
            ]
            content = content.replace("{secondary_findings}", random.choice(secondary_findings))
        
        if "{complication}" in content:
            complications = [
                "Patient became unresponsive", "Vital signs deteriorated", "Equipment malfunction",
                "Access difficulty", "Patient became combative", "Allergic reaction"
            ]
            content = content.replace("{complication}", random.choice(complications))
        
        if "{deterioration}" in content:
            deteriorations = [
                "Decreased level of consciousness", "Hypotension", "Respiratory distress",
                "Cardiac arrhythmia", "Severe pain", "Neurological changes"
            ]
            content = content.replace("{deterioration}", random.choice(deteriorations))
        
        if "{issue}" in content:
            issues = [
                "Monitor malfunction", "IV pump failure", "Oxygen tank empty", "Radio communication lost",
                "Stretcher malfunction", "Defibrillator battery low"
            ]
            content = content.replace("{issue}", random.choice(issues))
        
        return content
    
    def generate_incident_report(self, incident_id, crew_id, incident_data=None):
        """Generate a comprehensive incident report"""
        
        report_id = self.generate_id(prefix="REPORT", length=8)
        timestamp = datetime.now()
        
        # Generate report sections
        narrative = self._generate_narrative_section(incident_data)
        assessment = self._generate_assessment_section(incident_data)
        treatment = self._generate_treatment_section(incident_data)
        outcome = self._generate_outcome_section(incident_data)
        
        report = {
            'report_id': report_id,
            'incident_id': incident_id,
            'crew_id': crew_id,
            'report_type': 'COMPREHENSIVE',
            'narrative': narrative,
            'assessment': assessment,
            'treatment': treatment,
            'outcome': outcome,
            'timestamp': timestamp,
            'is_complete': True,
            'requires_review': random.choice([True, False]),
            'created_timestamp': datetime.now()
        }
        
        # Validate and store
        if self.validate_data(report):
            self.add_to_generated_data(report)
        
        return report
    
    def _generate_narrative_section(self, incident_data=None):
        """Generate narrative section of incident report"""
        
        if incident_data:
            emergency_type = incident_data.get('emergency_type', 'Medical emergency')
            location = incident_data.get('location', {}).get('address', 'Richmond, VA')
        else:
            emergency_type = random.choice(['Cardiac arrest', 'Trauma', 'Medical emergency', 'Respiratory distress'])
            location = 'Richmond, VA'
        
        narratives = [
            f"Unit dispatched to {location} for {emergency_type.lower()}. Upon arrival, patient was found in {random.choice(['stable', 'unstable', 'critical'])} condition.",
            f"Responded to {emergency_type.lower()} at {location}. Scene was {random.choice(['safe', 'controlled', 'chaotic'])} upon arrival.",
            f"Dispatched for {emergency_type.lower()} in {location}. Patient assessment began immediately upon arrival."
        ]
        
        return random.choice(narratives)
    
    def _generate_assessment_section(self, incident_data=None):
        """Generate assessment section of incident report"""
        
        assessments = [
            "Primary survey revealed patent airway, adequate breathing, and present circulation. Secondary survey showed no additional injuries.",
            "Initial assessment indicated patient was alert and oriented. Vital signs were within normal limits.",
            "Patient assessment revealed altered mental status. Vital signs were stable but required monitoring.",
            "Comprehensive assessment completed. Patient was responsive to verbal stimuli with stable vital signs."
        ]
        
        return random.choice(assessments)
    
    def _generate_treatment_section(self, incident_data=None):
        """Generate treatment section of incident report"""
        
        treatments = [
            "Treatment included oxygen therapy and cardiac monitoring. Patient responded well to interventions.",
            "Interventions performed: IV access established, medications administered as indicated. Patient tolerated all treatments.",
            "Treatment plan included pain management and immobilization. Patient condition improved with interventions.",
            "Standard protocols followed including airway management and fluid resuscitation. All treatments successful."
        ]
        
        return random.choice(treatments)
    
    def _generate_outcome_section(self, incident_data=None):
        """Generate outcome section of incident report"""
        
        outcomes = [
            "Patient transported to hospital in stable condition. Handoff completed without complications.",
            "Patient condition improved during transport. Transferred to hospital staff without incident.",
            "Patient remained stable throughout transport. Successful transfer to receiving facility.",
            "Transport completed successfully. Patient admitted to hospital for further care."
        ]
        
        return random.choice(outcomes)
    
    def generate_batch(self, count=10, incident_ids=None, crew_ids=None):
        """Generate a batch of provider notes"""
        print(f"=== GENERATING {count} PROVIDER NOTES ===")
        
        notes = []
        
        for i in range(count):
            # Generate sample IDs if not provided
            incident_id = incident_ids[i] if incident_ids and i < len(incident_ids) else self.generate_id(prefix="INC", length=8)
            crew_id = crew_ids[i] if crew_ids and i < len(crew_ids) else self.generate_id(prefix="CREW", length=8)
            
            note = self.generate_provider_note(incident_id, crew_id)
            notes.append(note)
            
            print(f"\n=== NOTE {i+1} ===")
            print(f" ID: {note['note_id']}")
            print(f" Type: {note['note_category']}")
            print(f" Priority: {note['priority']}")
            print(f" Content: {note['content'][:80]}...")
            print(f" Urgent: {'Yes' if note['is_urgent'] else 'No'}")
        
        return notes
    
    def get_notes_by_incident(self, incident_id):
        """Get all notes for a specific incident"""
        return [note for note in self.generated_data if note['incident_id'] == incident_id]
    
    def get_urgent_notes(self):
        """Get all urgent notes"""
        return [note for note in self.generated_data if note['is_urgent']]
    
    def validate_data(self, note):
        """Validate provider note data"""
        required_fields = ['note_id', 'incident_id', 'crew_id', 'note_type', 'content', 'timestamp']
        
        for field in required_fields:
            if field not in note or note[field] is None:
                print(f"❌ Validation failed: Missing {field}")
                return False
        
        # Content validation
        if len(note['content']) < 10:
            print(f"❌ Validation failed: Content too short")
            return False
        
        # Priority validation
        valid_priorities = ["Low", "Medium", "High", "Critical"]
        if note['priority'] not in valid_priorities:
            print(f"❌ Validation failed: Invalid priority {note['priority']}")
            return False
        
        return True
    
    def get_statistics(self):
        """Get statistics about generated provider notes"""
        if not self.generated_data:
            return super().get_statistics()
        
        # Calculate statistics
        urgent_count = sum(1 for note in self.generated_data if note['is_urgent'])
        
        # Note type distribution
        type_counts = {}
        for note in self.generated_data:
            note_type = note['note_type']
            type_counts[note_type] = type_counts.get(note_type, 0) + 1
        
        # Priority distribution
        priority_counts = {}
        for note in self.generated_data:
            priority = note['priority']
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        return {
            'total_generated': len(self.generated_data),
            'generator_type': self.__class__.__name__,
            'urgent_notes': urgent_count,
            'regular_notes': len(self.generated_data) - urgent_count,
            'note_type_distribution': type_counts,
            'priority_distribution': priority_counts
        }


# Test function
def test_provider_notes_generation():
    """Test the provider notes generator functionality"""
    generator = ProviderNotesGenerator()
    
    # Generate sample incident and crew IDs
    incident_ids = [generator.generate_id(prefix="INC", length=8) for _ in range(3)]
    crew_ids = [generator.generate_id(prefix="CREW", length=8) for _ in range(3)]
    
    # Generate notes
    notes = generator.generate_batch(5, incident_ids, crew_ids)
    
    # Test incident report generation
    if incident_ids:
        report = generator.generate_incident_report(incident_ids[0], crew_ids[0])
        print(f"\n=== INCIDENT REPORT ===")
        print(f" Report ID: {report['report_id']}")
        print(f" Narrative: {report['narrative']}")
        print(f" Assessment: {report['assessment']}")
        print(f" Treatment: {report['treatment']}")
        print(f" Outcome: {report['outcome']}")
    
    # Test filtering
    if incident_ids:
        incident_notes = generator.get_notes_by_incident(incident_ids[0])
        print(f"\n=== NOTES FOR INCIDENT {incident_ids[0]} ===")
        print(f" Count: {len(incident_notes)}")
    
    urgent_notes = generator.get_urgent_notes()
    print(f"\n=== URGENT NOTES ===")
    print(f" Count: {len(urgent_notes)}")
    
    # Print statistics
    stats = generator.get_statistics()
    print(f"\n=== PROVIDER NOTES STATISTICS ===")
    for key, value in stats.items():
        print(f" {key}: {value}")


if __name__ == "__main__":
    test_provider_notes_generation()
