"""
Crew Generator

Generates realistic EMS personnel data including names, shifts,
certifications, and unit assignments for the emergency services simulation.
"""

import random
from datetime import datetime, timedelta
from .base_generator import BaseGenerator


class CrewGenerator(BaseGenerator):
    """Generates EMS crew member data"""
    
    def __init__(self):
        super().__init__()
        
        # EMS Certifications and Roles
        self.certifications = [
            "EMT-Basic", "EMT-Intermediate", "EMT-Paramedic",
            "Critical Care Paramedic", "Flight Paramedic"
        ]
        
        self.roles = [
            "EMT", "Paramedic", "Field Supervisor", "Training Officer",
            "Field Training Officer", "Lieutenant", "Captain"
        ]
        
        self.shift_types = [
            "Day Shift (06:00-18:00)", "Night Shift (18:00-06:00)",
            "Swing Shift (14:00-02:00)", "24-Hour Shift"
        ]
        
        self.departments = [
            "Richmond Fire Department", "Richmond Ambulance Authority",
            "Henrico County Fire", "Chesterfield County Fire",
            "Virginia Commonwealth University Health"
        ]
    
    def generate_crew_member(self):
        """Generate a single crew member with complete information"""
        
        # Basic demographics - ensure age allows for reasonable experience
        age = random.randint(25, 65)  # Minimum 25 to allow for reasonable experience
        sex = random.choice(['M', 'F'])
        
        # Generate appropriate name based on age and sex
        if sex == 'M':
            name = self.fake.name_male()
        else:
            name = self.fake.name_female()
        
        # EMS-specific data
        certification = random.choice(self.certifications)
        role = random.choice(self.roles)
        department = random.choice(self.departments)
        
        # Experience and training - ensure experience doesn't exceed possible years
        max_possible_experience = age - 18
        years_experience = random.randint(1, min(25, max_possible_experience))
        hire_date = datetime.now() - timedelta(days=random.randint(365, 9125))  # 1-25 years
        
        # Contact information
        phone = self.fake.phone_number()
        email = self.fake.email()
        
        # Current status
        is_active = random.choice([True, True, True, False])  # 75% active
        current_shift = random.choice(self.shift_types) if is_active else None
        
        crew_member = {
            'crew_id': self.generate_id(prefix="CREW", length=8),
            'name': name,
            'age': age,
            'sex': sex,
            'certification': certification,
            'role': role,
            'department': department,
            'years_experience': years_experience,
            'hire_date': hire_date,
            'phone': phone,
            'email': email,
            'is_active': is_active,
            'current_shift': current_shift,
            'assigned_unit': None,  # Will be set by unit generator
            'created_timestamp': datetime.now()
        }
        
        # Validate and store
        if self.validate_data(crew_member):
            self.add_to_generated_data(crew_member)
        
        return crew_member
    
    def generate_shift_schedule(self, crew_id, start_date=None, days=7):
        """Generate a weekly shift schedule for a crew member"""
        
        if start_date is None:
            start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        schedule = []
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            # Randomly assign shifts (some days off)
            if random.random() < 0.8:  # 80% chance of working
                shift_type = random.choice(self.shift_types)
                
                # Determine shift hours based on type
                if "Day" in shift_type:
                    start_time = "06:00"
                    end_time = "18:00"
                elif "Night" in shift_type:
                    start_time = "18:00"
                    end_time = "06:00"
                elif "Swing" in shift_type:
                    start_time = "14:00"
                    end_time = "02:00"
                else:  # 24-hour
                    start_time = "06:00"
                    end_time = "06:00"
                
                schedule.append({
                    'schedule_id': self.generate_id(prefix="SCH", length=8),
                    'crew_id': crew_id,
                    'date': current_date.date(),
                    'shift_type': shift_type,
                    'start_time': start_time,
                    'end_time': end_time,
                    'is_working': True
                })
            else:
                schedule.append({
                    'schedule_id': self.generate_id(prefix="SCH", length=8),
                    'crew_id': crew_id,
                    'date': current_date.date(),
                    'shift_type': "Off Duty",
                    'start_time': None,
                    'end_time': None,
                    'is_working': False
                })
        
        return schedule
    
    def generate_batch(self, count=10):
        """Generate a batch of crew members"""
        print(f"=== GENERATING {count} CREW MEMBERS ===")
        
        crew_members = []
        for i in range(count):
            crew_member = self.generate_crew_member()
            crew_members.append(crew_member)
            
            print(f"\n=== CREW MEMBER {i+1} ===")
            print(f" ID: {crew_member['crew_id']}")
            print(f" Name: {crew_member['name']}")
            print(f" Role: {crew_member['role']} ({crew_member['certification']})")
            print(f" Department: {crew_member['department']}")
            print(f" Experience: {crew_member['years_experience']} years")
            print(f" Status: {'Active' if crew_member['is_active'] else 'Inactive'}")
        
        return crew_members
    
    def validate_data(self, crew_member):
        """Validate crew member data"""
        required_fields = ['crew_id', 'name', 'age', 'certification', 'role']
        
        for field in required_fields:
            if field not in crew_member or crew_member[field] is None:
                print(f"❌ Validation failed: Missing {field}")
                return False
        
        # Age validation
        if crew_member['age'] < 18 or crew_member['age'] > 70:
            print(f"❌ Validation failed: Invalid age {crew_member['age']}")
            return False
        
        # Experience validation - years_experience should not exceed possible working years
        max_possible_experience = crew_member['age'] - 18
        if crew_member['years_experience'] > max_possible_experience:
            print(f"❌ Validation failed: Experience ({crew_member['years_experience']} years) exceeds possible years ({max_possible_experience}) for age {crew_member['age']}")
            return False
        
        return True
    
    def get_statistics(self):
        """Get statistics about generated crew data"""
        if not self.generated_data:
            return super().get_statistics()
        
        # Calculate statistics
        active_count = sum(1 for crew in self.generated_data if crew['is_active'])
        avg_experience = sum(crew['years_experience'] for crew in self.generated_data) / len(self.generated_data)
        
        # Certification distribution
        cert_counts = {}
        for crew in self.generated_data:
            cert = crew['certification']
            cert_counts[cert] = cert_counts.get(cert, 0) + 1
        
        return {
            'total_generated': len(self.generated_data),
            'generator_type': self.__class__.__name__,
            'active_crew': active_count,
            'inactive_crew': len(self.generated_data) - active_count,
            'average_experience_years': round(avg_experience, 1),
            'certification_distribution': cert_counts
        }


# Test function
def test_crew_generation():
    """Test the crew generator functionality"""
    generator = CrewGenerator()
    
    # Generate a few crew members
    crew_members = generator.generate_batch(3)
    
    # Generate schedules for first crew member
    if crew_members:
        schedule = generator.generate_shift_schedule(crew_members[0]['crew_id'])
        print(f"\n=== SCHEDULE FOR {crew_members[0]['name']} ===")
        for day in schedule:
            print(f" {day['date']}: {day['shift_type']}")
    
    # Print statistics
    stats = generator.get_statistics()
    print(f"\n=== CREW STATISTICS ===")
    for key, value in stats.items():
        print(f" {key}: {value}")


if __name__ == "__main__":
    test_crew_generation()
