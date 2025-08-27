"""
Unit Generator

Generates realistic EMS unit data including unit types, locations,
availability status, and crew assignments for the emergency services simulation.
"""

import random
from datetime import datetime, timedelta
from .base_generator import BaseGenerator


class UnitGenerator(BaseGenerator):
    """Generates EMS unit data"""
    
    def __init__(self):
        super().__init__()
        
        # Unit Types and Capabilities
        self.unit_types = {
            "ALS": {
                "name": "Advanced Life Support",
                "crew_size": 2,
                "capabilities": ["IV Therapy", "Cardiac Monitoring", "Advanced Airway", "Medication Administration"],
                "vehicle_type": "Type I Ambulance"
            },
            "BLS": {
                "name": "Basic Life Support", 
                "crew_size": 2,
                "capabilities": ["Basic Assessment", "CPR", "Splinting", "Oxygen Therapy"],
                "vehicle_type": "Type III Ambulance"
            },
            "SUPERVISOR": {
                "name": "Field Supervisor",
                "crew_size": 1,
                "capabilities": ["Supervision", "Scene Management", "Quality Assurance"],
                "vehicle_type": "SUV/Command Vehicle"
            },
            "SPECIALTY": {
                "name": "Specialty Unit",
                "crew_size": 3,
                "capabilities": ["Critical Care", "Neonatal Transport", "Trauma Care"],
                "vehicle_type": "Critical Care Ambulance"
            }
        }
        
        # Unit Status Options
        self.status_options = [
            "Available", "En Route", "On Scene", "Transporting", 
            "At Hospital", "Returning", "Out of Service", "Maintenance"
        ]
        
        # Station Locations (Richmond area)
        self.stations = [
            {"name": "Station 1 - Downtown", "address": "100 N 7th St, Richmond, VA 23219"},
            {"name": "Station 2 - Fan District", "address": "200 W Cary St, Richmond, VA 23220"},
            {"name": "Station 3 - Museum District", "address": "300 W Franklin St, Richmond, VA 23220"},
            {"name": "Station 4 - Church Hill", "address": "400 N 25th St, Richmond, VA 23223"},
            {"name": "Station 5 - West End", "address": "500 Patterson Ave, Richmond, VA 23226"},
            {"name": "Station 6 - South Side", "address": "600 Hull St, Richmond, VA 23224"},
            {"name": "Station 7 - North Side", "address": "700 Chamberlayne Ave, Richmond, VA 23222"},
            {"name": "Station 8 - East End", "address": "800 Nine Mile Rd, Richmond, VA 23223"}
        ]
    
    def generate_unit(self, unit_type=None, assigned_crew=None):
        """Generate a single EMS unit with complete information"""
        
        # Determine unit type
        if unit_type is None:
            unit_type = random.choice(list(self.unit_types.keys()))
        
        unit_info = self.unit_types[unit_type]
        
        # Generate unit ID and name
        unit_id = self.generate_id(prefix=unit_type, length=6)
        unit_number = f"{unit_type}-{random.randint(1, 999):03d}"
        
        # Assign station
        station = random.choice(self.stations)
        
        # Current status and location
        status = random.choice(self.status_options)
        current_location = self.generate_richmond_coordinates()
        
        # Unit details
        vehicle_year = random.randint(2015, 2024)
        mileage = random.randint(50000, 150000)
        
        # Availability and timing
        is_available = status in ["Available", "Returning"]
        last_incident_time = None
        time_since_last_incident = None
        
        if not is_available:
            # Generate realistic timing for busy units
            last_incident_time = datetime.now() - timedelta(minutes=random.randint(5, 120))
            time_since_last_incident = datetime.now() - last_incident_time
        
        # Current assignment
        current_incident = None
        destination = None
        estimated_arrival = None
        
        if status in ["En Route", "On Scene", "Transporting"]:
            current_incident = self.generate_id(prefix="INC", length=8)
            destination = self.generate_richmond_address()
            
            if status == "En Route":
                # Calculate realistic ETA
                travel_time = random.randint(3, 15)  # minutes
                estimated_arrival = datetime.now() + timedelta(minutes=travel_time)
        
        unit = {
            'unit_id': unit_id,
            'unit_number': unit_number,
            'unit_type': unit_type,
            'unit_name': unit_info['name'],
            'crew_size': unit_info['crew_size'],
            'capabilities': unit_info['capabilities'],
            'vehicle_type': unit_info['vehicle_type'],
            'vehicle_year': vehicle_year,
            'mileage': mileage,
            'station': station['name'],
            'station_address': station['address'],
            'current_location': current_location,
            'status': status,
            'is_available': is_available,
            'assigned_crew': assigned_crew or [],
            'current_incident': current_incident,
            'destination': destination,
            'estimated_arrival': estimated_arrival,
            'last_incident_time': last_incident_time,
            'time_since_last_incident': time_since_last_incident,
            'created_timestamp': datetime.now()
        }
        
        # Validate and store
        if self.validate_data(unit):
            self.add_to_generated_data(unit)
        
        return unit
    
    def assign_crew_to_unit(self, unit, crew_members):
        """Assign crew members to a unit"""
        
        if not crew_members:
            return unit
        
        # Determine how many crew members needed
        required_crew = unit['crew_size']
        available_crew = [crew for crew in crew_members if crew['is_active'] and crew['assigned_unit'] is None]
        
        # Assign crew (up to the required number)
        assigned_crew = []
        for i in range(min(required_crew, len(available_crew))):
            crew = available_crew[i]
            crew['assigned_unit'] = unit['unit_id']
            assigned_crew.append(crew['crew_id'])
        
        unit['assigned_crew'] = assigned_crew
        return unit
    
    def update_unit_status(self, unit, new_status, incident_id=None, destination=None):
        """Update unit status and related information"""
        
        unit['status'] = new_status
        unit['is_available'] = new_status in ["Available", "Returning"]
        
        if new_status in ["En Route", "On Scene", "Transporting"]:
            unit['current_incident'] = incident_id
            if destination:
                unit['destination'] = destination
            
            if new_status == "En Route":
                travel_time = random.randint(3, 15)
                unit['estimated_arrival'] = datetime.now() + timedelta(minutes=travel_time)
        
        elif new_status == "Available":
            unit['current_incident'] = None
            unit['destination'] = None
            unit['estimated_arrival'] = None
            unit['last_incident_time'] = datetime.now()
        
        unit['updated_timestamp'] = datetime.now()
        return unit
    
    def generate_batch(self, count=8, crew_members=None):
        """Generate a batch of EMS units"""
        print(f"=== GENERATING {count} EMS UNITS ===")
        
        units = []
        
        # Ensure we have a good mix of unit types
        unit_types = list(self.unit_types.keys())
        for i in range(count):
            unit_type = unit_types[i % len(unit_types)] if i < len(unit_types) else random.choice(unit_types)
            
            unit = self.generate_unit(unit_type=unit_type)
            
            # Assign crew if available
            if crew_members:
                unit = self.assign_crew_to_unit(unit, crew_members)
            
            units.append(unit)
            
            print(f"\n=== UNIT {i+1} ===")
            print(f" ID: {unit['unit_id']}")
            print(f" Number: {unit['unit_number']}")
            print(f" Type: {unit['unit_name']}")
            print(f" Station: {unit['station']}")
            print(f" Status: {unit['status']}")
            print(f" Available: {'Yes' if unit['is_available'] else 'No'}")
            if unit['assigned_crew']:
                print(f" Crew: {len(unit['assigned_crew'])} assigned")
        
        return units
    
    def get_available_units(self):
        """Get all currently available units"""
        return [unit for unit in self.generated_data if unit['is_available']]
    
    def get_units_by_type(self, unit_type):
        """Get all units of a specific type"""
        return [unit for unit in self.generated_data if unit['unit_type'] == unit_type]
    
    def validate_data(self, unit):
        """Validate unit data"""
        required_fields = ['unit_id', 'unit_number', 'unit_type', 'status', 'is_available']
        
        for field in required_fields:
            if field not in unit or unit[field] is None:
                print(f"❌ Validation failed: Missing {field}")
                return False
        
        # Status validation
        if unit['status'] not in self.status_options:
            print(f"❌ Validation failed: Invalid status {unit['status']}")
            return False
        
        # Unit type validation
        if unit['unit_type'] not in self.unit_types:
            print(f"❌ Validation failed: Invalid unit type {unit['unit_type']}")
            return False
        
        return True
    
    def get_statistics(self):
        """Get statistics about generated unit data"""
        if not self.generated_data:
            return super().get_statistics()
        
        # Calculate statistics
        available_count = sum(1 for unit in self.generated_data if unit['is_available'])
        
        # Unit type distribution
        type_counts = {}
        for unit in self.generated_data:
            unit_type = unit['unit_type']
            type_counts[unit_type] = type_counts.get(unit_type, 0) + 1
        
        # Status distribution
        status_counts = {}
        for unit in self.generated_data:
            status = unit['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            'total_generated': len(self.generated_data),
            'generator_type': self.__class__.__name__,
            'available_units': available_count,
            'busy_units': len(self.generated_data) - available_count,
            'unit_type_distribution': type_counts,
            'status_distribution': status_counts
        }


# Test function
def test_unit_generation():
    """Test the unit generator functionality"""
    generator = UnitGenerator()
    
    # Generate units
    units = generator.generate_batch(6)
    
    # Test status updates
    if units:
        unit = units[0]
        print(f"\n=== TESTING STATUS UPDATE ===")
        print(f" Original status: {unit['status']}")
        
        updated_unit = generator.update_unit_status(
            unit, 
            "En Route", 
            incident_id="INC12345",
            destination="123 Main St, Richmond, VA"
        )
        print(f" Updated status: {updated_unit['status']}")
        print(f" Current incident: {updated_unit['current_incident']}")
    
    # Print statistics
    stats = generator.get_statistics()
    print(f"\n=== UNIT STATISTICS ===")
    for key, value in stats.items():
        print(f" {key}: {value}")


if __name__ == "__main__":
    test_unit_generation()
