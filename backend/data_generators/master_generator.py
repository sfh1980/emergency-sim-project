"""
Master Generator

Coordinates all specialized generators to create comprehensive emergency
services simulation data with realistic relationships between incidents,
crew, units, hospitals, and provider notes.
"""

import random
from datetime import datetime, timedelta
from .base_generator import BaseGenerator
from .incident_generator import IncidentGenerator
from .crew_generator import CrewGenerator
from .unit_generator import UnitGenerator
from .hospital_generator import HospitalGenerator
from .provider_notes_generator import ProviderNotesGenerator


class MasterGenerator(BaseGenerator):
    """Coordinates all data generators to create comprehensive simulation data"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize all generators
        self.incident_generator = IncidentGenerator()
        self.crew_generator = CrewGenerator()
        self.unit_generator = UnitGenerator()
        self.hospital_generator = HospitalGenerator()
        self.provider_notes_generator = ProviderNotesGenerator()
        
        # Store generated data by type
        self.incidents = []
        self.crew_members = []
        self.units = []
        self.hospitals = []
        self.provider_notes = []
        
        # Simulation state
        self.simulation_start_time = datetime.now()
        self.current_time = self.simulation_start_time
    
    def generate_complete_simulation(self, 
                                   incident_count=10, 
                                   crew_count=15, 
                                   unit_count=8, 
                                   hospital_count=5,
                                   notes_per_incident=3):
        """Generate a complete emergency services simulation"""
        
        print("🚨 === GENERATING COMPLETE EMERGENCY SERVICES SIMULATION ===")
        print(f"📊 Target: {incident_count} incidents, {crew_count} crew, {unit_count} units, {hospital_count} hospitals")
        
        # Step 1: Generate hospitals first (they're static)
        print("\n🏥 Step 1: Generating Hospitals...")
        self.hospitals = self.hospital_generator.generate_batch(hospital_count)
        
        # Step 2: Generate crew members
        print("\n👥 Step 2: Generating Crew Members...")
        self.crew_members = self.crew_generator.generate_batch(crew_count)
        
        # Step 3: Generate units and assign crew
        print("\n🚑 Step 3: Generating Units and Assigning Crew...")
        self.units = self.unit_generator.generate_batch(unit_count, self.crew_members)
        
        # Step 4: Generate incidents
        print("\n🚨 Step 4: Generating Incidents...")
        self.incidents = self.incident_generator.generate_batch(incident_count)
        
        # Step 5: Generate provider notes for each incident
        print("\n📝 Step 5: Generating Provider Notes...")
        self._generate_provider_notes_for_incidents(notes_per_incident)
        
        # Step 6: Create relationships and update statuses
        print("\n🔗 Step 6: Creating Relationships and Updating Statuses...")
        self._create_relationships()
        
        print("\n✅ === SIMULATION GENERATION COMPLETE ===")
        
        return {
            'incidents': self.incidents,
            'crew_members': self.crew_members,
            'units': self.units,
            'hospitals': self.hospitals,
            'provider_notes': self.provider_notes
        }
    
    def _generate_provider_notes_for_incidents(self, notes_per_incident):
        """Generate provider notes for each incident"""
        
        for incident in self.incidents:
            incident_id = incident['incident_id']
            
            # Find crew assigned to this incident (if any)
            assigned_crew = self._find_crew_for_incident(incident_id)
            crew_id = assigned_crew['crew_id'] if assigned_crew else self.generate_id(prefix="CREW", length=8)
            
            # Generate notes for this incident
            for i in range(notes_per_incident):
                # Determine note type based on sequence
                if i == 0:
                    note_type = "ARRIVAL"
                elif i == 1:
                    note_type = "ASSESSMENT"
                elif i == 2:
                    note_type = random.choice(["TREATMENT", "TRANSPORT"])
                else:
                    note_type = random.choice(["TREATMENT", "TRANSPORT", "HANDOFF", "COMPLICATION"])
                
                # Create context for the note
                context = {
                    'unit_id': self._find_unit_for_incident(incident_id),
                    'hospital': self._select_hospital_for_incident(incident),
                    'incident_type': incident['emergency_type']
                }
                
                # Generate the note
                note = self.provider_notes_generator.generate_provider_note(
                    incident_id, crew_id, note_type, context
                )
                self.provider_notes.append(note)
    
    def _create_relationships(self):
        """Create relationships between incidents, units, crew, and hospitals"""
        
        for incident in self.incidents:
            # Assign a unit to the incident
            available_units = [unit for unit in self.units if unit['is_available']]
            if available_units:
                assigned_unit = random.choice(available_units)
                incident['assigned_unit'] = assigned_unit['unit_id']
                
                # Update unit status
                self.unit_generator.update_unit_status(
                    assigned_unit, 
                    "En Route", 
                    incident['incident_id'],
                    incident['location']['address']
                )
                
                # Assign crew to the unit if not already assigned
                if not assigned_unit['assigned_crew']:
                    available_crew = [crew for crew in self.crew_members if crew['is_active'] and crew['assigned_unit'] is None]
                    if available_crew:
                        crew_to_assign = random.choice(available_crew)
                        crew_to_assign['assigned_unit'] = assigned_unit['unit_id']
                        assigned_unit['assigned_crew'].append(crew_to_assign['crew_id'])
            
            # Assign a destination hospital
            incident['destination_hospital'] = self._select_hospital_for_incident(incident)
    
    def _find_crew_for_incident(self, incident_id):
        """Find crew assigned to a specific incident"""
        # This is a simplified lookup - in a real system, you'd track assignments
        for unit in self.units:
            if unit.get('current_incident') == incident_id and unit['assigned_crew']:
                crew_id = unit['assigned_crew'][0]
                for crew in self.crew_members:
                    if crew['crew_id'] == crew_id:
                        return crew
        return None
    
    def _find_unit_for_incident(self, incident_id):
        """Find unit assigned to a specific incident"""
        for unit in self.units:
            if unit.get('current_incident') == incident_id:
                return unit['unit_number']
        return f"Unit-{random.randint(1, 999):03d}"
    
    def _select_hospital_for_incident(self, incident):
        """Select appropriate hospital for incident based on type and location"""
        
        # Determine if specialty hospital is needed
        specialty_needed = None
        if "Cardiac" in incident['emergency_type'] or "Heart" in incident['emergency_type']:
            specialty_needed = "CARDIAC"
        elif incident['caller_info']['age'] < 18:
            specialty_needed = "PEDIATRIC"
        elif "Trauma" in incident['emergency_type'] or "Car accident" in incident['emergency_type']:
            specialty_needed = "TRAUMA"
        
        # Find appropriate hospitals
        if specialty_needed:
            specialty_hospitals = [h for h in self.hospitals if h['hospital_type'] == specialty_needed]
            if specialty_hospitals:
                return random.choice(specialty_hospitals)['name']
        
        # Fall back to general hospitals
        general_hospitals = [h for h in self.hospitals if h['hospital_type'] == "GENERAL"]
        if general_hospitals:
            return random.choice(general_hospitals)['name']
        
        # Last resort - any available hospital
        available_hospitals = [h for h in self.hospitals if h['ed_status'] != "Critical"]
        if available_hospitals:
            return random.choice(available_hospitals)['name']
        
        return "VCU Medical Center"  # Default
    
    def get_simulation_statistics(self):
        """Get comprehensive statistics for the entire simulation"""
        
        stats = {
            'simulation_info': {
                'start_time': self.simulation_start_time,
                'current_time': self.current_time,
                'duration': self.current_time - self.simulation_start_time
            },
            'incidents': self.incident_generator.get_statistics(),
            'crew': self.crew_generator.get_statistics(),
            'units': self.unit_generator.get_statistics(),
            'hospitals': self.hospital_generator.get_statistics(),
            'provider_notes': self.provider_notes_generator.get_statistics(),
            'relationships': {
                'incidents_with_units': len([i for i in self.incidents if 'assigned_unit' in i]),
                'incidents_with_hospitals': len([i for i in self.incidents if 'destination_hospital' in i]),
                'units_with_crew': len([u for u in self.units if u['assigned_crew']]),
                'active_incidents': len([i for i in self.incidents if i.get('status') == 'dispatched'])
            }
        }
        
        return stats
    
    def get_incident_timeline(self, incident_id):
        """Get complete timeline for a specific incident"""
        
        # Find the incident
        incident = next((i for i in self.incidents if i['incident_id'] == incident_id), None)
        if not incident:
            return None
        
        # Get all related data
        timeline = {
            'incident': incident,
            'assigned_unit': next((u for u in self.units if u['unit_id'] == incident.get('assigned_unit')), None),
            'assigned_crew': [],
            'destination_hospital': next((h for h in self.hospitals if h['name'] == incident.get('destination_hospital')), None),
            'provider_notes': [n for n in self.provider_notes if n['incident_id'] == incident_id]
        }
        
        # Get crew information
        if timeline['assigned_unit']:
            for crew_id in timeline['assigned_unit']['assigned_crew']:
                crew = next((c for c in self.crew_members if c['crew_id'] == crew_id), None)
                if crew:
                    timeline['assigned_crew'].append(crew)
        
        return timeline
    
    def export_simulation_data(self):
        """Export all simulation data in a structured format"""
        
        return {
            'metadata': {
                'generated_at': datetime.now(),
                'simulation_id': self.generate_id(prefix="SIM", length=8),
                'total_entities': len(self.incidents) + len(self.crew_members) + len(self.units) + len(self.hospitals) + len(self.provider_notes)
            },
            'data': {
                'incidents': self.incidents,
                'crew_members': self.crew_members,
                'units': self.units,
                'hospitals': self.hospitals,
                'provider_notes': self.provider_notes
            },
            'statistics': self.get_simulation_statistics()
        }
    
    def print_simulation_summary(self):
        """Print a comprehensive summary of the simulation"""
        
        stats = self.get_simulation_statistics()
        
        print("\n" + "="*60)
        print("📊 EMERGENCY SERVICES SIMULATION SUMMARY")
        print("="*60)
        
        print(f"\n🚨 INCIDENTS:")
        print(f"   Total: {stats['incidents']['total_generated']}")
        print(f"   Priority Distribution: {stats['incidents']['priority_distribution']}")
        print(f"   Active: {stats['relationships']['active_incidents']}")
        
        print(f"\n👥 CREW:")
        print(f"   Total: {stats['crew']['total_generated']}")
        print(f"   Active: {stats['crew']['active_crew']}")
        print(f"   Average Experience: {stats['crew']['average_experience_years']} years")
        
        print(f"\n🚑 UNITS:")
        print(f"   Total: {stats['units']['total_generated']}")
        print(f"   Available: {stats['units']['available_units']}")
        print(f"   Busy: {stats['units']['busy_units']}")
        
        print(f"\n🏥 HOSPITALS:")
        print(f"   Total: {stats['hospitals']['total_generated']}")
        print(f"   Total Capacity: {stats['hospitals']['total_capacity']}")
        print(f"   Utilization: {stats['hospitals']['utilization_rate']}%")
        
        print(f"\n📝 PROVIDER NOTES:")
        print(f"   Total: {stats['provider_notes']['total_generated']}")
        print(f"   Urgent: {stats['provider_notes']['urgent_notes']}")
        
        print(f"\n🔗 RELATIONSHIPS:")
        print(f"   Incidents with Units: {stats['relationships']['incidents_with_units']}")
        print(f"   Incidents with Hospitals: {stats['relationships']['incidents_with_hospitals']}")
        print(f"   Units with Crew: {stats['relationships']['units_with_crew']}")
        
        print("\n" + "="*60)


# Test function
def test_master_generation():
    """Test the master generator functionality"""
    generator = MasterGenerator()
    
    # Generate a small simulation
    simulation_data = generator.generate_complete_simulation(
        incident_count=5,
        crew_count=8,
        unit_count=4,
        hospital_count=3,
        notes_per_incident=2
    )
    
    # Print summary
    generator.print_simulation_summary()
    
    # Test incident timeline
    if simulation_data['incidents']:
        incident_id = simulation_data['incidents'][0]['incident_id']
        timeline = generator.get_incident_timeline(incident_id)
        
        print(f"\n=== TIMELINE FOR INCIDENT {incident_id} ===")
        print(f" Emergency Type: {timeline['incident']['emergency_type']}")
        print(f" Assigned Unit: {timeline['assigned_unit']['unit_number'] if timeline['assigned_unit'] else 'None'}")
        print(f" Crew Members: {len(timeline['assigned_crew'])}")
        print(f" Destination Hospital: {timeline['destination_hospital']['name'] if timeline['destination_hospital'] else 'None'}")
        print(f" Provider Notes: {len(timeline['provider_notes'])}")
    
    # Export data
    export_data = generator.export_simulation_data()
    print(f"\n=== EXPORT SUMMARY ===")
    print(f" Simulation ID: {export_data['metadata']['simulation_id']}")
    print(f" Total Entities: {export_data['metadata']['total_entities']}")


if __name__ == "__main__":
    test_master_generation()
