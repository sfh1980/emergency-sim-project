"""
Database Setup for Emergency Services Simulation

Creates and configures both SQL Server and MongoDB databases
for the complete emergency services simulation platform.
"""

import pyodbc
import pymongo
from database_schemas import get_sql_schema, get_mongodb_schema, get_sql_indexes


class DatabaseSetup:
    """Handles database setup for both SQL Server and MongoDB"""
    
    def __init__(self):
        self.sql_connection = None
        self.mongo_client = None
        self.mongo_db = None
        
    def setup_sql_server(self):
        """Setup SQL Server database and tables"""
        try:
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
            
            print("✅ Connected to EmergencyMock database")
            
            # Get schema definitions
            sql_schema = get_sql_schema()
            sql_indexes = get_sql_indexes()
            
            # Create tables
            print("\n📊 Creating SQL Server tables...")
            for table_name, create_statement in sql_schema.items():
                try:
                    print(f"   Creating {table_name} table...")
                    cursor.execute(create_statement)
                    print(f"   ✅ {table_name} table created successfully")
                except pyodbc.Error as e:
                    if "There is already an object named" in str(e):
                        print(f"   ⚠️  {table_name} table already exists")
                    else:
                        print(f"   ❌ Error creating {table_name} table: {e}")
            
            # Create indexes
            print("\n🔍 Creating SQL Server indexes...")
            for index_statement in sql_indexes:
                try:
                    cursor.execute(index_statement)
                    print(f"   ✅ Index created: {index_statement[:50]}...")
                except pyodbc.Error as e:
                    if "There is already an object named" in str(e):
                        print(f"   ⚠️  Index already exists")
                    else:
                        print(f"   ❌ Error creating index: {e}")
            
            self.sql_connection.commit()
            print("✅ SQL Server setup completed successfully")
            
        except Exception as e:
            print(f"❌ SQL Server setup failed: {e}")
            raise
    
    def setup_mongodb(self):
        """Setup MongoDB database and collections"""
        try:
            # Connect to MongoDB
            self.mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
            self.mongo_db = self.mongo_client["EmergencyMock"]
            
            print("✅ Connected to EmergencyMock MongoDB database")
            
            # Get MongoDB schema
            mongo_schema = get_mongodb_schema()
            
            # Create collections and indexes
            print("\n📄 Creating MongoDB collections and indexes...")
            for collection_name, schema_info in mongo_schema.items():
                try:
                    # Create collection if it doesn't exist
                    if collection_name not in self.mongo_db.list_collection_names():
                        self.mongo_db.create_collection(collection_name)
                        print(f"   ✅ Created collection: {collection_name}")
                    else:
                        print(f"   ⚠️  Collection {collection_name} already exists")
                    
                    # Create indexes
                    collection = self.mongo_db[collection_name]
                    for index_info in schema_info['indexes']:
                        try:
                            field_name = index_info['field']
                            index_type = index_info['type']
                            collection.create_index([(field_name, index_type)])
                            print(f"   ✅ Created index on {field_name} for {collection_name}")
                        except Exception as e:
                            print(f"   ⚠️  Index on {field_name} for {collection_name} already exists or failed: {e}")
                
                except Exception as e:
                    print(f"   ❌ Error setting up {collection_name}: {e}")
            
            print("✅ MongoDB setup completed successfully")
            
        except Exception as e:
            print(f"❌ MongoDB setup failed: {e}")
            raise
    
    def verify_setup(self):
        """Verify that all tables and collections were created successfully"""
        print("\n🔍 === VERIFYING DATABASE SETUP ===")
        
        # Verify SQL Server tables
        if self.sql_connection:
            cursor = self.sql_connection.cursor()
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE' 
                AND TABLE_CATALOG = 'EmergencyMock'
                ORDER BY TABLE_NAME
            """)
            sql_tables = [row[0] for row in cursor.fetchall()]
            
            print(f"\n📊 SQL Server Tables ({len(sql_tables)} found):")
            for table in sql_tables:
                print(f"   ✅ {table}")
        
        # Verify MongoDB collections
        if self.mongo_db is not None:
            mongo_collections = self.mongo_db.list_collection_names()
            
            print(f"\n📄 MongoDB Collections ({len(mongo_collections)} found):")
            for collection in mongo_collections:
                print(f"   ✅ {collection}")
        
        # Verify indexes
        if self.sql_connection:
            cursor = self.sql_connection.cursor()
            cursor.execute("""
                SELECT 
                    t.name AS table_name,
                    i.name AS index_name,
                    i.type_desc AS index_type
                FROM sys.indexes i
                INNER JOIN sys.tables t ON i.object_id = t.object_id
                WHERE t.type = 'U' 
                AND i.name IS NOT NULL
                ORDER BY t.name, i.name
            """)
            sql_indexes = cursor.fetchall()
            
            print(f"\n🔍 SQL Server Indexes ({len(sql_indexes)} found):")
            current_table = ""
            for table, index, index_type in sql_indexes:
                if table != current_table:
                    print(f"   📋 {table}:")
                    current_table = table
                print(f"      ✅ {index} ({index_type})")
    
    def close_connections(self):
        """Close database connections"""
        if self.sql_connection:
            self.sql_connection.close()
            print("✅ SQL Server connection closed")
        
        if self.mongo_client:
            self.mongo_client.close()
            print("✅ MongoDB connection closed")
    
    def setup_complete_database(self):
        """Setup both SQL Server and MongoDB databases"""
        print("🚨 === EMERGENCY SERVICES DATABASE SETUP ===")
        
        try:
            # Setup SQL Server
            print("\n📊 Setting up SQL Server...")
            self.setup_sql_server()
            
            # Setup MongoDB
            print("\n📄 Setting up MongoDB...")
            self.setup_mongodb()
            
            # Verify setup
            self.verify_setup()
            
            print("\n✅ === DATABASE SETUP COMPLETE ===")
            print("🗄️  Both SQL Server and MongoDB are ready for the emergency services simulation!")
            
        except Exception as e:
            print(f"\n❌ Database setup failed: {e}")
            raise
        finally:
            self.close_connections()


def main():
    """Main function to run database setup"""
    setup = DatabaseSetup()
    setup.setup_complete_database()


if __name__ == "__main__":
    main()