"""
Test Data Generators

This script tests all data generators to ensure they create realistic and valid data
for the emergency services simulation platform.
"""

import sys
import os
from datetime import datetime

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from data_generators.incident_generator import IncidentGenerator
from data_generators.crew_generator import CrewGenerator
from data_generators.unit_generator import UnitGenerator
from data_generators.hospital_generator import HospitalGenerator
from data_generators.provider_notes_generator import ProviderNotesGenerator
from data_generators.master_generator import MasterGenerator

def test_incident_generator():
    """Test incident data generation"""
    print("🔍 === TESTING INCIDENT GENERATOR ===")
    
    try:
        generator = IncidentGenerator()
        incident = generator.generate_incident()
        
        # Validate required fields
        required_fields = ['incident_id', 'timestamp', 'caller_info', 'location', 
                          'emergency_type', 'priority', 'status']
        
        for field in required_fields:
            if field not in incident:
                print(f"❌ Missing required field: {field}")
                return False
            print(f"✅ {field}: {incident[field]}")
        
        # Validate nested structures
        if 'caller_info' in incident and 'name' in incident['caller_info']:
            print(f"✅ caller_name: {incident['caller_info']['name']}")
        else:
            print("❌ Missing caller_name in caller_info")
            return False
        
        # Validate data types and ranges
        if not isinstance(incident['priority'], int) or incident['priority'] < 1 or incident['priority'] > 5:
            print(f"❌ Invalid priority: {incident['priority']}")
            return False
        
        if not isinstance(incident['timestamp'], datetime):
            print(f"❌ Invalid timestamp type: {type(incident['timestamp'])}")
            return False
        
        print("✅ Incident generator test passed")
        return True
        
    except Exception as e:
        print(f"❌ Incident generator test failed: {e}")
        return False

def test_crew_generator():
    """Test crew member data generation"""
    print("\n🔍 === TESTING CREW GENERATOR ===")
    
    try:
        generator = CrewGenerator()
        crew = generator.generate_crew_member()
        
        # Validate required fields
        required_fields = ['crew_id', 'name', 'role', 'certification', 'years_experience']
        
        for field in required_fields:
            if field not in crew:
                print(f"❌ Missing required field: {field}")
                return False
            print(f"✅ {field}: {crew[field]}")
        
        # Validate role types
        valid_roles = ['EMT', 'Paramedic', 'Field Supervisor', 'Training Officer', 'Field Training Officer', 'Lieutenant', 'Captain']
        if crew['role'] not in valid_roles:
            print(f"❌ Invalid role: {crew['role']}")
            return False
        
        # Validate experience range
        if not isinstance(crew['years_experience'], int) or crew['years_experience'] < 0 or crew['years_experience'] > 30:
            print(f"❌ Invalid experience years: {crew['years_experience']}")
            return False
        
        print("✅ Crew generator test passed")
        return True
        
    except Exception as e:
        print(f"❌ Crew generator test failed: {e}")
        return False

def test_unit_generator():
    """Test EMS unit data generation"""
    print("\n🔍 === TESTING UNIT GENERATOR ===")
    
    try:
        generator = UnitGenerator()
        unit = generator.generate_unit()
        
        # Validate required fields
        required_fields = ['unit_id', 'unit_type', 'status', 'current_location', 'crew_size']
        
        for field in required_fields:
            if field not in unit:
                print(f"❌ Missing required field: {field}")
                return False
            print(f"✅ {field}: {unit[field]}")
        
        # Validate unit types
        valid_types = ['ALS', 'BLS', 'SUPERVISOR', 'SPECIALTY']
        if unit['unit_type'] not in valid_types:
            print(f"❌ Invalid unit type: {unit['unit_type']}")
            return False
        
        # Validate status types
        valid_statuses = ['Available', 'En Route', 'On Scene', 'Transporting', 'At Hospital', 'Returning', 'Out of Service', 'Maintenance']
        if unit['status'] not in valid_statuses:
            print(f"❌ Invalid status: {unit['status']}")
            return False
        
        print("✅ Unit generator test passed")
        return True
        
    except Exception as e:
        print(f"❌ Unit generator test failed: {e}")
        return False

def test_hospital_generator():
    """Test hospital data generation"""
    print("\n🔍 === TESTING HOSPITAL GENERATOR ===")
    
    try:
        generator = HospitalGenerator()
        hospital = generator.generate_hospital()
        
        # Validate required fields
        required_fields = ['hospital_id', 'name', 'address', 'hospital_type', 'level']
        
        for field in required_fields:
            if field not in hospital:
                print(f"❌ Missing required field: {field}")
                return False
            print(f"✅ {field}: {hospital[field]}")
        
        # Validate hospital type
        valid_types = ['TRAUMA', 'GENERAL', 'PEDIATRIC', 'CARDIAC']
        if hospital['hospital_type'] not in valid_types:
            print(f"❌ Invalid hospital type: {hospital['hospital_type']}")
            return False
        
        # Validate level
        valid_levels = ['Level I', 'Level II', 'Level III', 'Community', 'Specialized']
        if hospital['level'] not in valid_levels:
            print(f"❌ Invalid level: {hospital['level']}")
            return False
        
        print("✅ Hospital generator test passed")
        return True
        
    except Exception as e:
        print(f"❌ Hospital generator test failed: {e}")
        return False

def test_provider_notes_generator():
    """Test provider notes generation"""
    print("\n🔍 === TESTING PROVIDER NOTES GENERATOR ===")
    
    try:
        generator = ProviderNotesGenerator()
        notes = generator.generate_provider_note("TEST_INCIDENT", "TEST_CREW")
        
        # Validate required fields
        required_fields = ['note_id', 'incident_id', 'crew_id', 'note_type', 'content']
        
        for field in required_fields:
            if field not in notes:
                print(f"❌ Missing required field: {field}")
                return False
            print(f"✅ {field}: {notes[field]}")
        
        # Validate note type
        valid_types = ['ARRIVAL', 'ASSESSMENT', 'TREATMENT', 'TRANSPORT', 'HANDOFF', 'COMPLICATION']
        if notes['note_type'] not in valid_types:
            print(f"❌ Invalid note type: {notes['note_type']}")
            return False
        
        print("✅ Provider notes generator test passed")
        return True
        
    except Exception as e:
        print(f"❌ Provider notes generator test failed: {e}")
        return False

def test_master_generator():
    """Test master generator integration"""
    print("\n🔍 === TESTING MASTER GENERATOR ===")
    
    try:
        generator = MasterGenerator()
        
        # Test generating a small simulation with all related data
        complete_data = generator.generate_complete_simulation(
            incident_count=2,
            crew_count=3,
            unit_count=2,
            hospital_count=2,
            notes_per_incident=1
        )
        
        # Check that all components are present
        components = ['incidents', 'crew_members', 'units', 'hospitals', 'provider_notes']
        
        for component in components:
            if component not in complete_data:
                print(f"❌ Missing component: {component}")
                return False
            print(f"✅ {component}: Generated {len(complete_data[component])} items")
        
        # Validate data structure
        if len(complete_data['incidents']) > 0 and len(complete_data['provider_notes']) > 0:
            print("✅ Data relationships validated")
        
        print("✅ Master generator test passed")
        return True
        
    except Exception as e:
        print(f"❌ Master generator test failed: {e}")
        return False

def run_all_tests():
    """Run all generator tests"""
    print("🚀 === STARTING DATA GENERATOR TESTS ===\n")
    
    tests = [
        test_incident_generator,
        test_crew_generator,
        test_unit_generator,
        test_hospital_generator,
        test_provider_notes_generator,
        test_master_generator
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 === TEST RESULTS ===")
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed! Data generators are working correctly.")
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
    
    return passed == total

if __name__ == "__main__":
    run_all_tests()
