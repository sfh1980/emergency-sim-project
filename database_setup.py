"""
Database Setup Script for Emergency Services Mock App
This script creates the actual databases, tables, and collections
"""

import pyodbc
import pymongo
from database_schemas import SQL_SCHEMAS, MONGO_SCHEMAS
import json

class DatabaseSetup:
    def __init__(self):
        self.sql_connection = None
        self.mongo_client = None
        self.mongo_db = None
    
    def setup_sql_server(self):
        """Setup SQL Server database and tables"""
        try:
            print("=== SETTING UP SQL SERVER ===")
            print("Connecting to SQL Server...")
            
            # First connect to master database to create our database
            master_connection = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=localhost\\SQLEXPRESS;"
                "DATABASE=master;"
                "Trusted_Connection=yes;"
            )
            
            cursor = master_connection.cursor()
            
            # Set autocommit to allow CREATE DATABASE
            master_connection.autocommit = True
            
            # Create database if it doesn't exist
            print("Creating EmergencyMock database...")
            cursor.execute("""
                IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'EmergencyMock')
                BEGIN
                    CREATE DATABASE EmergencyMock
                END
            """)
            
            # Close connection to master
            master_connection.close()
            
            # Connect to our new database
            connection_string = (
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=localhost\\SQLEXPRESS;"
                "DATABASE=EmergencyMock;"
                "Trusted_Connection=yes;"
            )
            
            self.sql_connection = pyodbc.connect(connection_string)
            cursor = self.sql_connection.cursor()
            
            # Create tables
            for table_name, schema in SQL_SCHEMAS.items():
                print(f"Creating {table_name} table...")
                try:
                    cursor.execute(schema)
                    print(f"✅ {table_name} table created successfully")
                except pyodbc.Error as e:
                    print(f"⚠️  {table_name} table might already exist: {e}")
            
            self.sql_connection.commit()
            print("✅ SQL Server setup complete!")
            
        except Exception as e:
            print(f"❌ SQL Server setup failed: {e}")
            print("Make sure SQL Server is running and connection string is correct")
    
    def setup_mongodb(self):
        """Setup MongoDB database and collections"""
        try:
            print("\n=== SETTING UP MONGODB ===")
            print("Connecting to MongoDB...")
            
            # Connect to MongoDB
            self.mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
            self.mongo_db = self.mongo_client["EmergencyMock"]
            
            # Create collections and indexes
            for collection_name, schema_info in MONGO_SCHEMAS.items():
                print(f"Setting up {collection_name} collection...")
                
                # Create collection
                collection = self.mongo_db[schema_info['collection']]
                
                # Create indexes
                for index in schema_info['indexes']:
                    try:
                        collection.create_index(list(index.items()))
                        print(f"✅ Index created: {index}")
                    except Exception as e:
                        print(f"⚠️  Index might already exist: {e}")
                
                print(f"✅ {collection_name} collection ready")
            
            print("✅ MongoDB setup complete!")
            
        except Exception as e:
            print(f"❌ MongoDB setup failed: {e}")
            print("Make sure MongoDB is running on localhost:27017")
    
    def test_connections(self):
        """Test database connections"""
        print("\n=== TESTING CONNECTIONS ===")
        
        # Test SQL Server
        try:
            cursor = self.sql_connection.cursor()
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            print(f"✅ SQL Server connected: {version[:50]}...")
        except Exception as e:
            print(f"❌ SQL Server connection failed: {e}")
        
        # Test MongoDB
        try:
            result = self.mongo_client.admin.command('ping')
            print("✅ MongoDB connected successfully")
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
    
    def close_connections(self):
        """Close database connections"""
        if self.sql_connection:
            self.sql_connection.close()
        if self.mongo_client:
            self.mongo_client.close()
        print("Database connections closed")

def main():
    """Main setup function"""
    setup = DatabaseSetup()
    
    try:
        # Setup both databases
        setup.setup_sql_server()
        setup.setup_mongodb()
        
        # Test connections
        setup.test_connections()
        
        print("\n🎉 Database setup complete!")
        print("You can now run your incident generator and store data in the databases!")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
    
    finally:
        setup.close_connections()

if __name__ == "__main__":
    main()