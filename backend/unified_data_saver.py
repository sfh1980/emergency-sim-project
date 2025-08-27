"""
Unified Data Saver for Emergency Services Simulation Platform

Combines the working data_saver.py with enhanced_data_saver.py functionality.
Integrates with existing data generators for comprehensive data management.
"""

import pyodbc
import pymongo
from datetime import datetime, timedelta
import json
import uuid
import random

# Import data generators
from data_generators.incident_generator import IncidentGenerator
from data_generators.crew_generator import CrewGenerator
from data_generators.unit_generator import UnitGenerator
from data_generators.hospital_generator import HospitalGenerator
from data_generators.provider_notes_generator import ProviderNotesGenerator

# Import data adapter
from data_adapter import DataAdapter


class UnifiedDataSaver:
    """Unified data saver that handles all emergency services data types"""
    
    def __init__(self):
        self.sql_connection = None
        self.mongo_client = None
        self.mongo_db = None
        self.connect_databases()
        
        # Initialize data generators
        self.incident_generator = IncidentGenerator()
        self.crew_generator = CrewGenerator()
        self.unit_generator = UnitGenerator()
        self.hospital_generator = HospitalGenerator()
        self.notes_generator = ProviderNotesGenerator()
    
    def connect_databases(self):
        """Connect to both databases"""
        try:
            # Connect to SQL Server
            self.sql_connection = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=localhost\\SQLEXPRESS;"
                "DATABASE=EmergencyMock;"
                "Trusted_Connection=yes;"
            )
            
            # Connect to MongoDB
            self.mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
            self.mongo_db = self.mongo_client["EmergencyMock"]
            
            print("✅ Connected to both databases")
            
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise
    
    # ===== INCIDENTS (Working from data_saver.py) =====
    def save_incident_to_sql(self, incident):
        """Save incident to SQL Server (using working method from data_saver.py)"""
        cursor = self.sql_connection.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO incidents (
                    incident_id, caller_name, caller_age, caller_sex,
                    location_address, location_lat, location_lng,
                    emergency_type, priority, status, call_timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                incident['incident_id'],
                incident['caller_info']['name'],
                incident['caller_info']['age'],
                incident['caller_info']['sex'],
                incident['location']['address'],
                incident['location']['coordinates']['latitude'],
                incident['location']['coordinates']['longitude'],
                incident['emergency_type'],
                incident['priority'],
                'dispatched',
                incident['timestamp']
            ))
            
            self.sql_connection.commit()
            print(f"✅ Saved incident {incident['incident_id']} to SQL Server")
            
        except Exception as e:
            print(f"❌ Error saving to SQL Server: {e}")
    
    def save_incident_to_mongo(self, incident):
        """Save detailed incident to MongoDB (using working method from data_saver.py)"""
        try:
            incident_doc = {
                "incident_id": incident['incident_id'],
                "caller_info": incident['caller_info'],
                "location": incident['location'],
                "emergency_details": {
                    "type": incident['emergency_type'],
                    "priority": incident['priority'],
                    "symptoms": incident['symptoms'],
                    "vital_signs": incident['vital_signs']
                },
                "patient_condition": incident['patient_condition'],
                "operator_notes": incident['operator_notes'],
                "call_timestamp": incident['timestamp'].isoformat(),
                "created_at": datetime.now().isoformat()
            }
            
            collection = self.mongo_db["incident_details"]
            collection.insert_one(incident_doc)
            
            print(f"✅ Saved incident {incident['incident_id']} to MongoDB")
            
        except Exception as e:
            print(f"❌ Error saving to MongoDB: {e}")
    
    # ===== CREW MEMBERS =====
    def save_crew_member(self, crew_data):
        """Save crew member to SQL Server"""
        cursor = self.sql_connection.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO crew_members (
                    crew_id, first_name, last_name, certification_level,
                    years_experience, is_active, hire_date, phone_number,
                    email, emergency_contact, certifications, specializations
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                crew_data['crew_id'],
                crew_data['first_name'],
                crew_data['last_name'],
                crew_data['certification_level'],
                crew_data['years_experience'],
                crew_data['is_active'],
                crew_data['hire_date'],
                crew_data['phone_number'],
                crew_data['email'],
                crew_data['emergency_contact'],
                crew_data['certifications'],
                crew_data['specializations']
            ))
            
            self.sql_connection.commit()
            print(f"✅ Saved crew member {crew_data['crew_id']} to SQL Server")
            
        except Exception as e:
            print(f"❌ Error saving crew member to SQL Server: {e}")
    
    def save_crew_details_to_mongo(self, crew_data):
        """Save detailed crew information to MongoDB"""
        try:
            crew_doc = {
                "crew_id": crew_data['crew_id'],
                "personal_info": {
                    "first_name": crew_data['first_name'],
                    "last_name": crew_data['last_name'],
                    "phone_number": crew_data['phone_number'],
                    "email": crew_data['email'],
                    "emergency_contact": crew_data['emergency_contact']
                },
                "professional_info": {
                    "certification_level": crew_data['certification_level'],
                    "years_experience": crew_data['years_experience'],
                    "certifications": crew_data['certifications'],
                    "specializations": crew_data['specializations'],
                    "hire_date": crew_data['hire_date'].isoformat()
                },
                "status": {
                    "is_active": crew_data['is_active'],
                    "assigned_unit": crew_data.get('assigned_unit'),
                    "current_shift": crew_data.get('current_shift'),
                    "last_incident": crew_data.get('last_incident')
                },
                "performance_metrics": {
                    "total_incidents": crew_data.get('total_incidents', 0),
                    "response_time_avg": crew_data.get('response_time_avg', 0),
                    "patient_satisfaction": crew_data.get('patient_satisfaction', 0)
                },
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            collection = self.mongo_db["crew_details"]
            collection.insert_one(crew_doc)
            
            print(f"✅ Saved crew details {crew_data['crew_id']} to MongoDB")
            
        except Exception as e:
            print(f"❌ Error saving crew details to MongoDB: {e}")
    
    # ===== EMS UNITS =====
    def save_ems_unit(self, unit_data):
        """Save EMS unit to SQL Server"""
        cursor = self.sql_connection.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO ems_units (
                    unit_id, unit_number, unit_name, unit_type, vehicle_type, vehicle_year,
                    mileage, station, station_address, current_lat, current_lng, status, is_available,
                    current_incident, destination, estimated_arrival, last_incident_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                unit_data['unit_id'],
                unit_data['unit_number'],
                unit_data['unit_name'],
                unit_data['unit_type'],
                unit_data['vehicle_type'],
                unit_data['vehicle_year'],
                unit_data['mileage'],
                unit_data['station'],
                unit_data['station_address'],
                unit_data['current_lat'],
                unit_data['current_lng'],
                unit_data['status'],
                unit_data['is_available'],
                unit_data.get('current_incident'),
                unit_data.get('destination'),
                unit_data.get('estimated_arrival'),
                unit_data.get('last_incident_time')
            ))
            
            self.sql_connection.commit()
            print(f"✅ Saved EMS unit {unit_data['unit_id']} to SQL Server")
            
        except Exception as e:
            print(f"❌ Error saving EMS unit to SQL Server: {e}")
    
    def save_unit_status_to_mongo(self, unit_data):
        """Save unit status stream to MongoDB"""
        try:
            status_doc = {
                "unit_id": unit_data['unit_id'],
                "status": unit_data['status'],
                "is_available": unit_data['is_available'],
                "location": {
                    "station": unit_data['station'],
                    "station_address": unit_data['station_address'],
                    "current_location": unit_data.get('current_location'),
                    "destination": unit_data.get('destination')
                },
                "operational_info": {
                    "current_incident": unit_data.get('current_incident'),
                    "estimated_arrival": unit_data.get('estimated_arrival'),
                    "last_incident_time": unit_data.get('last_incident_time'),
                    "mileage": unit_data['mileage']
                },
                "vehicle_info": {
                    "vehicle_type": unit_data['vehicle_type'],
                    "vehicle_year": unit_data['vehicle_year'],
                    "unit_type": unit_data['unit_type']
                },
                "timestamp": datetime.now().isoformat(),
                "created_at": datetime.now().isoformat()
            }
            
            collection = self.mongo_db["unit_status_streams"]
            collection.insert_one(status_doc)
            
            print(f"✅ Saved unit status {unit_data['unit_id']} to MongoDB")
            
        except Exception as e:
            print(f"❌ Error saving unit status to MongoDB: {e}")
    
    # ===== HOSPITALS =====
    def save_hospital(self, hospital_data):
        """Save hospital to SQL Server"""
        cursor = self.sql_connection.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO hospitals (
                    hospital_id, hospital_name, address, phone_number,
                    hospital_type, level, total_capacity, current_capacity,
                    available_beds, ed_status, average_wait_time, trauma_level,
                    helicopter_pad, burn_unit, stroke_center, lat, lng
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                hospital_data['hospital_id'],
                hospital_data['hospital_name'],
                hospital_data['address'],
                hospital_data['phone_number'],
                hospital_data['hospital_type'],
                hospital_data['level'],
                hospital_data['total_capacity'],
                hospital_data['current_capacity'],
                hospital_data['available_beds'],
                hospital_data['ed_status'],
                hospital_data['average_wait_time'],
                hospital_data['trauma_level'],
                hospital_data['helicopter_pad'],
                hospital_data['burn_unit'],
                hospital_data['stroke_center'],
                hospital_data['lat'],
                hospital_data['lng']
            ))
            
            self.sql_connection.commit()
            print(f"✅ Saved hospital {hospital_data['hospital_id']} to SQL Server")
            
        except Exception as e:
            print(f"❌ Error saving hospital to SQL Server: {e}")
    
    def save_hospital_status_to_mongo(self, hospital_data):
        """Save hospital status to MongoDB"""
        try:
            status_doc = {
                "hospital_id": hospital_data['hospital_id'],
                "hospital_name": hospital_data['hospital_name'],
                "status": {
                    "hospital_type": hospital_data['hospital_type'],
                    "level": hospital_data['level'],
                    "trauma_level": hospital_data['trauma_level'],
                    "ed_status": hospital_data['ed_status']
                },
                "capacity": {
                    "total_capacity": hospital_data['total_capacity'],
                    "current_capacity": hospital_data['current_capacity'],
                    "available_beds": hospital_data['available_beds'],
                    "utilization_rate": round(hospital_data['current_capacity'] / hospital_data['total_capacity'] * 100, 2)
                },
                "capabilities": {
                    "helicopter_pad": hospital_data['helicopter_pad'],
                    "burn_unit": hospital_data['burn_unit'],
                    "stroke_center": hospital_data['stroke_center']
                },
                "performance": {
                    "average_wait_time": hospital_data['average_wait_time'],
                    "last_updated": datetime.now().isoformat()
                },
                "contact_info": {
                    "address": hospital_data['address'],
                    "phone_number": hospital_data['phone_number']
                },
                "timestamp": datetime.now().isoformat(),
                "created_at": datetime.now().isoformat()
            }
            
            collection = self.mongo_db["hospital_status"]
            collection.insert_one(status_doc)
            
            print(f"✅ Saved hospital status {hospital_data['hospital_id']} to MongoDB")
            
        except Exception as e:
            print(f"❌ Error saving hospital status to MongoDB: {e}")
    
    # ===== PROVIDER NOTES =====
    def save_provider_note(self, note_data):
        """Save provider note to SQL Server"""
        cursor = self.sql_connection.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO provider_notes (
                    note_id, incident_id, crew_id, note_type, note_content,
                    is_urgent, timestamp, created_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                note_data['note_id'],
                note_data['incident_id'],
                note_data['crew_id'],
                note_data['note_type'],
                note_data['note_content'],
                note_data['is_urgent'],
                note_data['timestamp'],
                note_data['created_by']
            ))
            
            self.sql_connection.commit()
            print(f"✅ Saved provider note {note_data['note_id']} to SQL Server")
            
        except Exception as e:
            print(f"❌ Error saving provider note to SQL Server: {e}")
    
    def save_provider_note_to_mongo(self, note_data):
        """Save provider note to MongoDB"""
        try:
            note_doc = {
                "note_id": note_data['note_id'],
                "incident_id": note_data['incident_id'],
                "crew_id": note_data['crew_id'],
                "note_type": note_data['note_type'],
                "note_content": note_data['note_content'],
                "metadata": {
                    "is_urgent": note_data['is_urgent'],
                    "created_by": note_data['created_by'],
                    "timestamp": note_data['timestamp'].isoformat()
                },
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            collection = self.mongo_db["provider_notes"]
            collection.insert_one(note_doc)
            
            print(f"✅ Saved provider note {note_data['note_id']} to MongoDB")
            
        except Exception as e:
            print(f"❌ Error saving provider note to MongoDB: {e}")
    
    # ===== COMPOSITE SAVE METHODS =====
    def save_incident_complete(self, incident):
        """Save incident to both databases"""
        print(f"\n=== SAVING INCIDENT {incident['incident_id']} ===")
        self.save_incident_to_sql(incident)
        self.save_incident_to_mongo(incident)
    
    def save_crew_complete(self, crew_data):
        """Save crew member to both databases"""
        print(f"\n=== SAVING CREW MEMBER {crew_data['crew_id']} ===")
        self.save_crew_member(crew_data)
        self.save_crew_details_to_mongo(crew_data)
    
    def save_unit_complete(self, unit_data):
        """Save EMS unit to both databases"""
        print(f"\n=== SAVING EMS UNIT {unit_data['unit_id']} ===")
        self.save_ems_unit(unit_data)
        self.save_unit_status_to_mongo(unit_data)
    
    def save_hospital_complete(self, hospital_data):
        """Save hospital to both databases"""
        print(f"\n=== SAVING HOSPITAL {hospital_data['hospital_id']} ===")
        self.save_hospital(hospital_data)
        self.save_hospital_status_to_mongo(hospital_data)
    
    def save_provider_note_complete(self, note_data):
        """Save provider note to both databases"""
        print(f"\n=== SAVING PROVIDER NOTE {note_data['note_id']} ===")
        self.save_provider_note(note_data)
        self.save_provider_note_to_mongo(note_data)
    
    def close_connections(self):
        """Close database connections"""
        if self.sql_connection:
            self.sql_connection.close()
        if self.mongo_client:
            self.mongo_client.close()
        print("✅ Database connections closed")


def test_unified_data_saving():
    """Test saving all data types using the unified data saver"""
    print("🚨 === TESTING UNIFIED DATA SAVING ===")
    
    # Create unified data saver
    saver = UnifiedDataSaver()
    
    # Test incidents (using working method)
    print("\n🚨 Testing incident saving...")
    for i in range(2):
        incident = saver.incident_generator.generate_incident()
        incident = DataAdapter.adapt_incident_data(incident)
        saver.save_incident_complete(incident)
    
    # Test crew members
    print("\n👥 Testing crew member saving...")
    for i in range(2):
        crew_data = saver.crew_generator.generate_crew_member()
        crew_data = DataAdapter.adapt_crew_data(crew_data)
        saver.save_crew_complete(crew_data)
    
    # Test EMS units
    print("\n🚑 Testing EMS unit saving...")
    for i in range(2):
        unit_data = saver.unit_generator.generate_unit()
        unit_data = DataAdapter.adapt_unit_data(unit_data)
        saver.save_unit_complete(unit_data)
    
    # Test hospitals
    print("\n🏥 Testing hospital saving...")
    for i in range(2):
        hospital_data = saver.hospital_generator.generate_hospital()
        hospital_data = DataAdapter.adapt_hospital_data(hospital_data)
        saver.save_hospital_complete(hospital_data)
    
    # Test provider notes
    print("\n📝 Testing provider note saving...")
    for i in range(2):
        note_data = saver.notes_generator.generate_provider_note(
            incident_id="INC_TEST001", 
            crew_id="CREW_TEST001"
        )
        note_data = DataAdapter.adapt_provider_note_data(note_data)
        saver.save_provider_note_complete(note_data)
    
    saver.close_connections()
    print("\n🎉 Unified data saving test complete!")


if __name__ == "__main__":
    test_unified_data_saving()
