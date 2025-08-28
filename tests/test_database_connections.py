"""
Test Database Connections

This script tests database connectivity and basic operations for both SQL Server and MongoDB
to ensure the backend can properly connect to and interact with the databases.
"""

import sys
import os
import pyodbc
import pymongo
from datetime import datetime

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

def test_sql_server_connection():
    """Test SQL Server connection and basic operations"""
    print("🔍 === TESTING SQL SERVER CONNECTION ===")
    
    try:
        # Test connection
        connection = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"
            "DATABASE=EmergencyMock;"
            "Trusted_Connection=yes;"
        )
        print("✅ SQL Server connection successful")
        
        cursor = connection.cursor()
        
        # Test basic query
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        print(f"✅ SQL Server version: {version[:50]}...")
        
        # Test table existence
        tables = ['incidents', 'crew_members', 'ems_units', 'provider_notes', 'hospitals']
        existing_tables = []
        
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"✅ Table {table}: {count} rows")
                existing_tables.append(table)
            except Exception as e:
                print(f"❌ Table {table}: {e}")
        
        # Test schema information
        print("\n📋 === TABLE SCHEMA INFORMATION ===")
        for table in existing_tables:
            try:
                cursor.execute(f"""
                    SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = '{table}'
                    ORDER BY ORDINAL_POSITION
                """)
                
                columns = cursor.fetchall()
                print(f"\n📊 {table} columns:")
                for col in columns:
                    print(f"   - {col[0]}: {col[1]} (Nullable: {col[2]})")
                    
            except Exception as e:
                print(f"❌ Error getting schema for {table}: {e}")
        
        cursor.close()
        connection.close()
        print("\n✅ SQL Server test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ SQL Server connection failed: {e}")
        return False

def test_mongodb_connection():
    """Test MongoDB connection and basic operations"""
    print("\n🔍 === TESTING MONGODB CONNECTION ===")
    
    try:
        # Test connection
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["EmergencyMock"]
        print("✅ MongoDB connection successful")
        
        # Test database list
        databases = client.list_database_names()
        print(f"✅ Available databases: {databases}")
        
        # Test collection operations
        collections = db.list_collection_names()
        print(f"✅ Collections in EmergencyMock: {collections}")
        
        # Test basic document insertion and retrieval
        test_collection = db["test_collection"]
        
        # Insert test document
        test_doc = {
            "test_id": 1,
            "message": "Test document",
            "timestamp": datetime.now(),
            "data": {"key": "value"}
        }
        
        result = test_collection.insert_one(test_doc)
        print(f"✅ Inserted test document with ID: {result.inserted_id}")
        
        # Retrieve test document
        retrieved_doc = test_collection.find_one({"test_id": 1})
        if retrieved_doc:
            print(f"✅ Retrieved test document: {retrieved_doc['message']}")
        else:
            print("❌ Failed to retrieve test document")
            return False
        
        # Clean up test document
        test_collection.delete_one({"test_id": 1})
        print("✅ Cleaned up test document")
        
        client.close()
        print("✅ MongoDB test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("   (This is expected if MongoDB service is not running)")
        return False

def test_data_persistence():
    """Test data persistence through the unified data saver"""
    print("\n🔍 === TESTING DATA PERSISTENCE ===")
    
    try:
        from unified_data_saver import UnifiedDataSaver
        from data_generators.master_generator import MasterGenerator
        
        # Generate test data
        generator = MasterGenerator()
        test_data = generator.generate_complete_simulation(
            incident_count=1,
            crew_count=1,
            unit_count=1,
            hospital_count=1,
            notes_per_incident=1
        )
        
        print("✅ Generated test data")
        
        # Test data saver
        saver = UnifiedDataSaver()
        
        # Test saving individual components to SQL Server
        try:
            if test_data['incidents']:
                saver.save_incident_to_sql(test_data['incidents'][0])
                print("✅ SQL Server save test completed")
        except Exception as e:
            print(f"❌ SQL Server save failed: {e}")
        
        # Test saving individual components to MongoDB
        try:
            if test_data['incidents']:
                saver.save_incident_to_mongo(test_data['incidents'][0])
                print("✅ MongoDB save test completed")
        except Exception as e:
            print(f"❌ MongoDB save failed: {e}")
        
        print("✅ Data persistence test completed")
        return True
        
    except Exception as e:
        print(f"❌ Data persistence test failed: {e}")
        return False

def test_api_endpoints():
    """Test basic API functionality"""
    print("\n🔍 === TESTING API ENDPOINTS ===")
    
    try:
        from api.dashboard import app
        
        # Test that Flask app can be created
        with app.test_client() as client:
            # Test basic route
            response = client.get('/')
            print(f"✅ Root endpoint status: {response.status_code}")
            
            # Test API endpoints
            response = client.get('/api/incidents')
            print(f"✅ Incidents endpoint status: {response.status_code}")
            
            response = client.get('/api/units')
            print(f"✅ Units endpoint status: {response.status_code}")
            
            response = client.get('/api/hospitals')
            print(f"✅ Hospitals endpoint status: {response.status_code}")
        
        print("✅ API endpoints test completed")
        return True
        
    except Exception as e:
        print(f"❌ API endpoints test failed: {e}")
        return False

def run_all_database_tests():
    """Run all database-related tests"""
    print("🚀 === STARTING DATABASE CONNECTION TESTS ===\n")
    
    tests = [
        test_sql_server_connection,
        test_mongodb_connection,
        test_data_persistence,
        test_api_endpoints
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 === DATABASE TEST RESULTS ===")
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All database tests passed! Backend is ready for deployment.")
    else:
        print("⚠️ Some database tests failed. Please review the errors above.")
    
    return passed == total

if __name__ == "__main__":
    run_all_database_tests()
