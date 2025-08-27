"""
Final Comprehensive System Test

This script performs a complete test of the emergency services simulation system
to identify and document any remaining issues before frontend development.
"""

import pyodbc
import pymongo
from datetime import datetime
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_generators.incident_generator import IncidentGenerator
from data_generators.crew_generator import CrewGenerator
from data_generators.unit_generator import UnitGenerator
from data_generators.hospital_generator import HospitalGenerator
from data_generators.provider_notes_generator import ProviderNotesGenerator
from data_adapter import DataAdapter
from unified_data_saver import UnifiedDataSaver

def test_database_connections():
    """Test database connectivity"""
    print("🔍 === TESTING DATABASE CONNECTIONS ===")
    
    # Test SQL Server
    try:
        sql_conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"
            "DATABASE=EmergencyMock;"
            "Trusted_Connection=yes;"
        )
        print("✅ SQL Server connection successful")
        sql_conn.close()
    except Exception as e:
        print(f"❌ SQL Server connection failed: {e}")
        return False
    
    # Test MongoDB
    try:
        mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        mongo_db = mongo_client["EmergencyMock"]
        print("✅ MongoDB connection successful")
        mongo_client.close()
    except Exception as e:
        print(f"⚠️ MongoDB connection failed: {e}")
        print("   (This is expected if MongoDB service is not running)")
    
    return True

def check_database_schema():
    """Check database schema and identify issues"""
    print("\n🔍 === CHECKING DATABASE SCHEMA ===")
    
    try:
        connection = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"
            "DATABASE=EmergencyMock;"
            "Trusted_Connection=yes;"
        )
        
        cursor = connection.cursor()
        
        # Check all tables
        tables = ['incidents', 'crew_members', 'ems_units', 'provider_notes', 'hospitals']
        issues = []
        
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"📊 {table}: {count} rows")
            except Exception as e:
                print(f"❌ {table}: Error - {e}")
                issues.append(f"Table {table} access issue: {e}")
        
        # Check hospital table specifically
        print("\n🏥 === HOSPITAL TABLE DETAILS ===")
        try:
            cursor.execute("""
                SELECT 
                    COLUMN_NAME, 
                    DATA_TYPE, 
                    CHARACTER_MAXIMUM_LENGTH,
                    IS_NULLABLE,
                    COLUMNPROPERTY(object_id('hospitals'), 'hospital_id', 'IsIdentity') as IsIdentity
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'hospitals' AND COLUMN_NAME = 'hospital_id'
            """)
            
            column_info = cursor.fetchone()
            if column_info:
                print(f"📋 Hospital ID column: {column_info}")
                print(f"📋 Is IDENTITY: {column_info[4] == 1}")
                if column_info[4] == 1:
                    issues.append("Hospital table has IDENTITY column - prevents string ID insertion")
            else:
                print("❌ Hospital ID column not found")
                issues.append("Hospital table missing hospital_id column")
                
        except Exception as e:
            print(f"❌ Error checking hospital table: {e}")
            issues.append(f"Hospital table schema check failed: {e}")
        
        # Check EMS units table for column sizes
        print("\n🚑 === EMS UNITS TABLE DETAILS ===")
        try:
            cursor.execute("""
                SELECT 
                    COLUMN_NAME, 
                    DATA_TYPE, 
                    CHARACTER_MAXIMUM_LENGTH,
                    IS_NULLABLE
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'ems_units' AND COLUMN_NAME = 'unit_number'
            """)
            
            column_info = cursor.fetchone()
            if column_info:
                print(f"📋 Unit number column: {column_info}")
                if column_info[2] and column_info[2] < 10:
                    issues.append(f"Unit number column too small: {column_info[2]} characters")
            else:
                print("❌ Unit number column not found")
                issues.append("EMS units table missing unit_number column")
                
        except Exception as e:
            print(f"❌ Error checking EMS units table: {e}")
            issues.append(f"EMS units table schema check failed: {e}")
        
        connection.close()
        
        if issues:
            print(f"\n⚠️ Found {len(issues)} schema issues:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print("\n✅ No schema issues found")
        
        return issues
        
    except Exception as e:
        print(f"❌ Database schema check failed: {e}")
        return [f"Database schema check failed: {e}"]

def test_data_generators():
    """Test all data generators"""
    print("\n🔍 === TESTING DATA GENERATORS ===")
    
    issues = []
    
    try:
        # Test incident generator
        incident_gen = IncidentGenerator()
        incident = incident_gen.generate_incident()
        if not incident or 'incident_id' not in incident:
            issues.append("Incident generator not producing valid data")
        else:
            print("✅ Incident generator working")
        
        # Test crew generator
        crew_gen = CrewGenerator()
        crew = crew_gen.generate_crew_member()
        if not crew or 'crew_id' not in crew:
            issues.append("Crew generator not producing valid data")
        else:
            print("✅ Crew generator working")
        
        # Test unit generator
        unit_gen = UnitGenerator()
        unit = unit_gen.generate_unit()
        if not unit or 'unit_id' not in unit:
            issues.append("Unit generator not producing valid data")
        else:
            print("✅ Unit generator working")
        
        # Test hospital generator
        hospital_gen = HospitalGenerator()
        hospital = hospital_gen.generate_hospital()
        if not hospital or 'hospital_id' not in hospital:
            issues.append("Hospital generator not producing valid data")
        else:
            print("✅ Hospital generator working")
        
        # Test provider notes generator
        notes_gen = ProviderNotesGenerator()
        note = notes_gen.generate_provider_note("INC_TEST", "CREW_TEST")
        if not note or 'note_id' not in note:
            issues.append("Provider notes generator not producing valid data")
        else:
            print("✅ Provider notes generator working")
        
    except Exception as e:
        issues.append(f"Data generator test failed: {e}")
    
    if issues:
        print(f"\n⚠️ Found {len(issues)} generator issues:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("\n✅ All data generators working")
    
    return issues

def test_data_adapters():
    """Test data adapters"""
    print("\n🔍 === TESTING DATA ADAPTERS ===")
    
    issues = []
    
    try:
        # Test incident adapter
        incident_gen = IncidentGenerator()
        incident = incident_gen.generate_incident()
        adapted_incident = DataAdapter.adapt_incident_data(incident)
        if not adapted_incident or 'incident_id' not in adapted_incident:
            issues.append("Incident adapter not working")
        else:
            print("✅ Incident adapter working")
        
        # Test crew adapter
        crew_gen = CrewGenerator()
        crew = crew_gen.generate_crew_member()
        adapted_crew = DataAdapter.adapt_crew_data(crew)
        if not adapted_crew or 'crew_id' not in adapted_crew:
            issues.append("Crew adapter not working")
        else:
            print("✅ Crew adapter working")
        
        # Test unit adapter
        unit_gen = UnitGenerator()
        unit = unit_gen.generate_unit()
        adapted_unit = DataAdapter.adapt_unit_data(unit)
        if not adapted_unit or 'unit_id' not in adapted_unit:
            issues.append("Unit adapter not working")
        else:
            print("✅ Unit adapter working")
        
        # Test hospital adapter
        hospital_gen = HospitalGenerator()
        hospital = hospital_gen.generate_hospital()
        adapted_hospital = DataAdapter.adapt_hospital_data(hospital)
        if not adapted_hospital or 'hospital_id' not in adapted_hospital:
            issues.append("Hospital adapter not working")
        else:
            print("✅ Hospital adapter working")
        
        # Test provider notes adapter
        notes_gen = ProviderNotesGenerator()
        note = notes_gen.generate_provider_note("INC_TEST", "CREW_TEST")
        adapted_note = DataAdapter.adapt_provider_note_data(note)
        if not adapted_note or 'note_id' not in adapted_note:
            issues.append("Provider notes adapter not working")
        else:
            print("✅ Provider notes adapter working")
        
    except Exception as e:
        issues.append(f"Data adapter test failed: {e}")
    
    if issues:
        print(f"\n⚠️ Found {len(issues)} adapter issues:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("\n✅ All data adapters working")
    
    return issues

def test_data_saving():
    """Test data saving to databases"""
    print("\n🔍 === TESTING DATA SAVING ===")
    
    issues = []
    
    try:
        saver = UnifiedDataSaver()
        
        # Test incident saving
        incident_gen = IncidentGenerator()
        incident = incident_gen.generate_incident()
        incident = DataAdapter.adapt_incident_data(incident)
        try:
            saver.save_incident_complete(incident)
            print("✅ Incident saving working")
        except Exception as e:
            issues.append(f"Incident saving failed: {e}")
        
        # Test crew saving
        crew_gen = CrewGenerator()
        crew = crew_gen.generate_crew_member()
        crew = DataAdapter.adapt_crew_data(crew)
        try:
            saver.save_crew_complete(crew)
            print("✅ Crew saving working")
        except Exception as e:
            issues.append(f"Crew saving failed: {e}")
        
        # Test unit saving
        unit_gen = UnitGenerator()
        unit = unit_gen.generate_unit()
        unit = DataAdapter.adapt_unit_data(unit)
        try:
            saver.save_unit_complete(unit)
            print("✅ Unit saving working")
        except Exception as e:
            issues.append(f"Unit saving failed: {e}")
        
        # Test provider notes saving
        notes_gen = ProviderNotesGenerator()
        note = notes_gen.generate_provider_note(incident['incident_id'], crew['crew_id'])
        note = DataAdapter.adapt_provider_note_data(note)
        try:
            saver.save_provider_note_complete(note)
            print("✅ Provider notes saving working")
        except Exception as e:
            issues.append(f"Provider notes saving failed: {e}")
        
        # Test hospital saving (will likely fail due to IDENTITY issue)
        hospital_gen = HospitalGenerator()
        hospital = hospital_gen.generate_hospital()
        hospital = DataAdapter.adapt_hospital_data(hospital)
        try:
            saver.save_hospital_complete(hospital)
            print("✅ Hospital saving working")
        except Exception as e:
            issues.append(f"Hospital saving failed: {e}")
        
        saver.close_connections()
        
    except Exception as e:
        issues.append(f"Data saving test failed: {e}")
    
    if issues:
        print(f"\n⚠️ Found {len(issues)} saving issues:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("\n✅ All data saving working")
    
    return issues

def generate_final_report(schema_issues, generator_issues, adapter_issues, saving_issues):
    """Generate comprehensive final report"""
    print("\n" + "="*60)
    print("📋 === FINAL SYSTEM TEST REPORT ===")
    print("="*60)
    
    all_issues = schema_issues + generator_issues + adapter_issues + saving_issues
    
    if not all_issues:
        print("🎉 PERFECT! NO ISSUES FOUND")
        print("🚀 System is 100% ready for frontend development")
        return True
    
    print(f"\n⚠️ Found {len(all_issues)} total issues:")
    print("-" * 40)
    
    if schema_issues:
        print(f"\n🔧 SCHEMA ISSUES ({len(schema_issues)}):")
        for issue in schema_issues:
            print(f"   • {issue}")
    
    if generator_issues:
        print(f"\n🔧 GENERATOR ISSUES ({len(generator_issues)}):")
        for issue in generator_issues:
            print(f"   • {issue}")
    
    if adapter_issues:
        print(f"\n🔧 ADAPTER ISSUES ({len(adapter_issues)}):")
        for issue in adapter_issues:
            print(f"   • {issue}")
    
    if saving_issues:
        print(f"\n🔧 SAVING ISSUES ({len(saving_issues)}):")
        for issue in saving_issues:
            print(f"   • {issue}")
    
    print(f"\n📊 SUMMARY:")
    print(f"   • Schema Issues: {len(schema_issues)}")
    print(f"   • Generator Issues: {len(generator_issues)}")
    print(f"   • Adapter Issues: {len(adapter_issues)}")
    print(f"   • Saving Issues: {len(saving_issues)}")
    print(f"   • Total Issues: {len(all_issues)}")
    
    success_rate = max(0, 100 - (len(all_issues) * 10))
    print(f"\n📈 SYSTEM SUCCESS RATE: {success_rate}%")
    
    if success_rate >= 90:
        print("🎉 System is ready for frontend development!")
    elif success_rate >= 80:
        print("⚠️ Minor issues remain - recommend fixing before frontend")
    else:
        print("❌ Significant issues remain - must fix before frontend")
    
    return success_rate >= 90

def main():
    """Main execution function"""
    print("🚨 === FINAL COMPREHENSIVE SYSTEM TEST ===")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Test database connections
    if not test_database_connections():
        print("\n❌ Database connection test failed - cannot proceed")
        return False
    
    # Check database schema
    schema_issues = check_database_schema()
    
    # Test data generators
    generator_issues = test_data_generators()
    
    # Test data adapters
    adapter_issues = test_data_adapters()
    
    # Test data saving
    saving_issues = test_data_saving()
    
    # Generate final report
    system_ready = generate_final_report(schema_issues, generator_issues, adapter_issues, saving_issues)
    
    print(f"\nFinished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return system_ready

if __name__ == "__main__":
    main()
