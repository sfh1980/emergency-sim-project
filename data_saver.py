"""
Data Saver for Emergency Services Mock App
This script saves generated incidents to both SQL Server and MongoDB
"""

import pyodbc
import pymongo
from datetime import datetime
import json
from incident_generator import Incident, IncidentBatchGenerator

class DataSaver:
    def __init__(self):
        self.sql_connection = None
        self.mongo_client = None
        self.mongo_db = None
        self.connect_databases()
    
    def connect_databases(self):
        """Connect to both databases"""
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
    
    def save_incident_to_sql(self, incident):
        """Save incident to SQL Server"""
        cursor = self.sql_connection.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO incidents (
                    incident_id, caller_name, caller_age, caller_sex,
                    location_address, location_lat, location_lng,
                    emergency_type, priority, status, call_timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                incident.incident_id,
                incident.caller_info['name'],
                incident.caller_info['age'],
                incident.caller_info['sex'],
                incident.location['address'],
                incident.location['coordinates']['latitude'],
                incident.location['coordinates']['longitude'],
                incident.emergency_type,
                incident.priority,
                'dispatched',
                incident.timestamp
            ))
            
            self.sql_connection.commit()
            print(f"✅ Saved incident {incident.incident_id} to SQL Server")
            
        except Exception as e:
            print(f"❌ Error saving to SQL Server: {e}")
    
    def save_incident_to_mongo(self, incident):
        """Save detailed incident to MongoDB"""
        try:
            # Prepare the document
            incident_doc = {
                "incident_id": incident.incident_id,
                "caller_info": incident.caller_info,
                "location": incident.location,
                "emergency_details": {
                    "type": incident.emergency_type,
                    "priority": incident.priority,
                    "symptoms": incident.symptoms,
                    "vital_signs": incident.vital_signs
                },
                "patient_condition": incident.patient_condition,
                "operator_notes": incident.operator_notes,
                "call_timestamp": incident.timestamp.isoformat(),
                "created_at": datetime.now().isoformat()
            }
            
            # Insert into MongoDB
            collection = self.mongo_db["incident_details"]
            collection.insert_one(incident_doc)
            
            print(f"✅ Saved incident {incident.incident_id} to MongoDB")
            
        except Exception as e:
            print(f"❌ Error saving to MongoDB: {e}")
    
    def save_incident(self, incident):
        """Save incident to both databases"""
        print(f"\n=== SAVING INCIDENT {incident.incident_id} ===")
        self.save_incident_to_sql(incident)
        self.save_incident_to_mongo(incident)
    
    def close_connections(self):
        """Close database connections"""
        if self.sql_connection:
            self.sql_connection.close()
        if self.mongo_client:
            self.mongo_client.close()
        print("Database connections closed")

def test_data_saving():
    """Test saving incidents to databases"""
    print("=== TESTING DATA SAVING ===")
    
    # Create data saver
    saver = DataSaver()
    
    # Generate and save a single incident
    incident = Incident()
    saver.save_incident(incident)
    
    # Generate and save multiple incidents
    generator = IncidentBatchGenerator()
    incidents = generator.generate_batch(3)
    
    for incident in incidents:
        saver.save_incident(incident)
    
    saver.close_connections()
    print("\n🎉 Data saving test complete!")

if __name__ == "__main__":
    test_data_saving()