"""
Hospital Generator

Generates realistic hospital data including specialties, wait times,
capacity, and location information for the emergency services simulation.
"""

import random
from datetime import datetime, timedelta
from .base_generator import BaseGenerator


class HospitalGenerator(BaseGenerator):
    """Generates hospital data"""
    
    def __init__(self):
        super().__init__()
        
        # Hospital Types and Specialties
        self.hospital_types = {
            "TRAUMA": {
                "name": "Trauma Center",
                "level": "Level I",
                "specialties": ["Trauma Surgery", "Emergency Medicine", "Orthopedics", "Neurosurgery"],
                "capacity": random.randint(200, 500),
                "wait_time_factor": 0.8  # Faster for trauma
            },
            "GENERAL": {
                "name": "General Hospital",
                "level": "Community",
                "specialties": ["Emergency Medicine", "Internal Medicine", "Cardiology", "General Surgery"],
                "capacity": random.randint(150, 300),
                "wait_time_factor": 1.0  # Standard wait times
            },
            "PEDIATRIC": {
                "name": "Children's Hospital",
                "level": "Specialized",
                "specialties": ["Pediatric Emergency", "Pediatric Surgery", "Neonatology", "Pediatric Cardiology"],
                "capacity": random.randint(100, 250),
                "wait_time_factor": 0.9  # Slightly faster for kids
            },
            "CARDIAC": {
                "name": "Cardiac Center",
                "level": "Specialized",
                "specialties": ["Cardiology", "Cardiac Surgery", "Emergency Medicine", "Interventional Cardiology"],
                "capacity": random.randint(120, 280),
                "wait_time_factor": 0.7  # Fast for cardiac
            }
        }
        
        # Richmond Area Hospitals
        self.hospital_locations = [
            {
                "name": "VCU Medical Center",
                "address": "1200 E Broad St, Richmond, VA 23219",
                "coordinates": {"latitude": 37.5407, "longitude": -77.4348},
                "type": "TRAUMA"
            },
            {
                "name": "Henrico Doctors' Hospital",
                "address": "1602 Skipwith Rd, Richmond, VA 23229",
                "coordinates": {"latitude": 37.6234, "longitude": -77.5678},
                "type": "GENERAL"
            },
            {
                "name": "St. Mary's Hospital",
                "address": "5801 Bremo Rd, Richmond, VA 23226",
                "coordinates": {"latitude": 37.5890, "longitude": -77.5234},
                "type": "GENERAL"
            },
            {
                "name": "Children's Hospital of Richmond",
                "address": "1000 E Broad St, Richmond, VA 23219",
                "coordinates": {"latitude": 37.5412, "longitude": -77.4356},
                "type": "PEDIATRIC"
            },
            {
                "name": "Chippenham Hospital",
                "address": "7101 Jahnke Rd, Richmond, VA 23225",
                "coordinates": {"latitude": 37.5123, "longitude": -77.4789},
                "type": "GENERAL"
            }
        ]
    
    def generate_hospital(self, hospital_type=None, location=None):
        """Generate a single hospital with complete information"""
        
        # Determine hospital type
        if hospital_type is None:
            hospital_type = random.choice(list(self.hospital_types.keys()))
        
        hospital_info = self.hospital_types[hospital_type]
        
        # Use provided location or generate one
        if location is None:
            location = random.choice(self.hospital_locations)
        
        # Generate hospital ID and details
        hospital_id = self.generate_id(prefix="HOSP", length=8)
        
        # Current capacity and wait times
        current_capacity = random.randint(int(hospital_info['capacity'] * 0.6), hospital_info['capacity'])
        available_beds = hospital_info['capacity'] - current_capacity
        
        # Calculate wait times based on capacity and type
        base_wait_time = random.randint(15, 120)  # minutes
        adjusted_wait_time = int(base_wait_time * hospital_info['wait_time_factor'])
        
        # Emergency department status
        ed_status = "Open"
        if available_beds < 10:
            ed_status = "Limited"
        elif available_beds < 5:
            ed_status = "Critical"
        
        # Generate specialties and services
        specialties = hospital_info['specialties'].copy()
        if random.random() < 0.3:  # 30% chance to add additional specialty
            additional_specialties = ["Oncology", "Neurology", "Psychiatry", "Urology", "Gynecology"]
            specialties.append(random.choice(additional_specialties))
        
        hospital = {
            'hospital_id': hospital_id,
            'name': location['name'],
            'hospital_type': hospital_type,
            'level': hospital_info['level'],
            'specialties': specialties,
            'address': location['address'],
            'coordinates': location['coordinates'],
            'phone': f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",  # Add phone field
            'total_capacity': hospital_info['capacity'],
            'current_capacity': current_capacity,
            'available_beds': available_beds,
            'ed_status': ed_status,
            'average_wait_time': adjusted_wait_time,
            'trauma_level': "Level I" if hospital_type == "TRAUMA" else "Level III",
            'helicopter_pad': hospital_type in ["TRAUMA", "CARDIAC"],
            'burn_unit': hospital_type == "TRAUMA",
            'stroke_center': hospital_type in ["TRAUMA", "CARDIAC"],
            'created_timestamp': datetime.now()
        }
        
        # Validate and store
        if self.validate_data(hospital):
            self.add_to_generated_data(hospital)
        
        return hospital
    
    def update_hospital_status(self, hospital, new_patients=0, discharged_patients=0):
        """Update hospital capacity and wait times"""
        
        # Update capacity
        hospital['current_capacity'] += new_patients - discharged_patients
        hospital['available_beds'] = hospital['total_capacity'] - hospital['current_capacity']
        
        # Update ED status based on new capacity
        if hospital['available_beds'] < 10:
            hospital['ed_status'] = "Limited"
        elif hospital['available_beds'] < 5:
            hospital['ed_status'] = "Critical"
        else:
            hospital['ed_status'] = "Open"
        
        # Update wait times based on capacity
        capacity_ratio = hospital['current_capacity'] / hospital['total_capacity']
        base_wait_time = random.randint(15, 120)
        
        if capacity_ratio > 0.9:
            wait_multiplier = 2.0  # Very busy
        elif capacity_ratio > 0.8:
            wait_multiplier = 1.5  # Busy
        elif capacity_ratio > 0.7:
            wait_multiplier = 1.2  # Moderately busy
        else:
            wait_multiplier = 1.0  # Normal
        
        hospital['average_wait_time'] = int(base_wait_time * wait_multiplier)
        hospital['updated_timestamp'] = datetime.now()
        
        return hospital
    
    def get_hospitals_by_specialty(self, specialty):
        """Get all hospitals that have a specific specialty"""
        return [hospital for hospital in self.generated_data if specialty in hospital['specialties']]
    
    def get_available_hospitals(self):
        """Get all hospitals that are accepting patients"""
        return [hospital for hospital in self.generated_data if hospital['ed_status'] != "Critical"]
    
    def get_closest_hospital(self, coordinates, specialty=None):
        """Get the closest hospital to given coordinates, optionally filtering by specialty"""
        import math
        
        available_hospitals = self.get_available_hospitals()
        
        if specialty:
            available_hospitals = self.get_hospitals_by_specialty(specialty)
        
        if not available_hospitals:
            return None
        
        # Calculate distances (simplified)
        closest_hospital = None
        min_distance = float('inf')
        
        for hospital in available_hospitals:
            hosp_coords = hospital['coordinates']
            distance = math.sqrt(
                (coordinates['latitude'] - hosp_coords['latitude']) ** 2 +
                (coordinates['longitude'] - hosp_coords['longitude']) ** 2
            )
            
            if distance < min_distance:
                min_distance = distance
                closest_hospital = hospital
        
        return closest_hospital
    
    def generate_batch(self, count=5):
        """Generate a batch of hospitals"""
        print(f"=== GENERATING {count} HOSPITALS ===")
        
        hospitals = []
        
        # Use predefined locations for realistic hospitals
        for i, location in enumerate(self.hospital_locations[:count]):
            hospital = self.generate_hospital(
                hospital_type=location['type'],
                location=location
            )
            hospitals.append(hospital)
            
            print(f"\n=== HOSPITAL {i+1} ===")
            print(f" ID: {hospital['hospital_id']}")
            print(f" Name: {hospital['name']}")
            print(f" Type: {hospital['hospital_type']} ({hospital['level']})")
            print(f" Status: {hospital['ed_status']}")
            print(f" Capacity: {hospital['current_capacity']}/{hospital['total_capacity']}")
            print(f" Wait Time: {hospital['average_wait_time']} minutes")
            print(f" Specialties: {', '.join(hospital['specialties'][:3])}")
        
        return hospitals
    
    def validate_data(self, hospital):
        """Validate hospital data"""
        required_fields = ['hospital_id', 'name', 'hospital_type', 'total_capacity', 'current_capacity']
        
        for field in required_fields:
            if field not in hospital or hospital[field] is None:
                print(f"❌ Validation failed: Missing {field}")
                return False
        
        # Capacity validation
        if hospital['current_capacity'] > hospital['total_capacity']:
            print(f"❌ Validation failed: Current capacity exceeds total capacity")
            return False
        
        if hospital['available_beds'] < 0:
            print(f"❌ Validation failed: Negative available beds")
            return False
        
        # Wait time validation
        if hospital['average_wait_time'] < 0:
            print(f"❌ Validation failed: Negative wait time")
            return False
        
        return True
    
    def get_statistics(self):
        """Get statistics about generated hospital data"""
        if not self.generated_data:
            return super().get_statistics()
        
        # Calculate statistics
        total_capacity = sum(hospital['total_capacity'] for hospital in self.generated_data)
        total_current = sum(hospital['current_capacity'] for hospital in self.generated_data)
        avg_wait_time = sum(hospital['average_wait_time'] for hospital in self.generated_data) / len(self.generated_data)
        
        # Status distribution
        status_counts = {}
        for hospital in self.generated_data:
            status = hospital['ed_status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Type distribution
        type_counts = {}
        for hospital in self.generated_data:
            hosp_type = hospital['hospital_type']
            type_counts[hosp_type] = type_counts.get(hosp_type, 0) + 1
        
        return {
            'total_generated': len(self.generated_data),
            'generator_type': self.__class__.__name__,
            'total_capacity': total_capacity,
            'total_current_capacity': total_current,
            'utilization_rate': round((total_current / total_capacity) * 100, 1),
            'average_wait_time_minutes': round(avg_wait_time, 1),
            'status_distribution': status_counts,
            'type_distribution': type_counts
        }


# Test function
def test_hospital_generation():
    """Test the hospital generator functionality"""
    generator = HospitalGenerator()
    
    # Generate hospitals
    hospitals = generator.generate_batch(4)
    
    # Test status updates
    if hospitals:
        hospital = hospitals[0]
        print(f"\n=== TESTING STATUS UPDATE ===")
        print(f" Original capacity: {hospital['current_capacity']}/{hospital['total_capacity']}")
        print(f" Original wait time: {hospital['average_wait_time']} minutes")
        
        updated_hospital = generator.update_hospital_status(hospital, new_patients=5, discharged_patients=2)
        print(f" Updated capacity: {updated_hospital['current_capacity']}/{updated_hospital['total_capacity']}")
        print(f" Updated wait time: {updated_hospital['average_wait_time']} minutes")
        print(f" ED Status: {updated_hospital['ed_status']}")
    
    # Test closest hospital
    test_coords = {"latitude": 37.5407, "longitude": -77.4348}
    closest = generator.get_closest_hospital(test_coords, specialty="Emergency Medicine")
    if closest:
        print(f"\n=== CLOSEST HOSPITAL ===")
        print(f" Name: {closest['name']}")
        print(f" Distance: Calculated from coordinates")
    
    # Print statistics
    stats = generator.get_statistics()
    print(f"\n=== HOSPITAL STATISTICS ===")
    for key, value in stats.items():
        print(f" {key}: {value}")


if __name__ == "__main__":
    test_hospital_generation()
