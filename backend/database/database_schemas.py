"""
Database Schemas for Emergency Services Simulation

Defines the structure for both SQL Server (relational) and MongoDB (document)
databases to support the complete emergency services simulation platform.
"""

# SQL Server Schema - Relational Database
SQL_SCHEMA = {
    # Existing tables
    "incidents": """
        CREATE TABLE incidents (
            incident_id VARCHAR(20) PRIMARY KEY,
            caller_name VARCHAR(100) NOT NULL,
            caller_age INT NOT NULL,
            caller_sex VARCHAR(10) NOT NULL,
            location_address VARCHAR(200) NOT NULL,
            location_lat DECIMAL(10, 6) NOT NULL,
            location_lng DECIMAL(10, 6) NOT NULL,
            emergency_type VARCHAR(100) NOT NULL,
            priority INT NOT NULL,
            status VARCHAR(50) DEFAULT 'dispatched',
            call_timestamp DATETIME2 NOT NULL,
            assigned_unit VARCHAR(20),
            destination_hospital VARCHAR(100),
            created_timestamp DATETIME2 DEFAULT GETDATE()
        )
    """,
    
    # New tables for expanded simulation
    "crew_members": """
        CREATE TABLE crew_members (
            crew_id VARCHAR(20) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT NOT NULL,
            sex VARCHAR(10) NOT NULL,
            certification VARCHAR(50) NOT NULL,
            role VARCHAR(50) NOT NULL,
            department VARCHAR(100) NOT NULL,
            years_experience INT NOT NULL,
            hire_date DATETIME2 NOT NULL,
            phone VARCHAR(20),
            email VARCHAR(100),
            is_active BIT DEFAULT 1,
            current_shift VARCHAR(50),
            assigned_unit VARCHAR(20),
            created_timestamp DATETIME2 DEFAULT GETDATE()
        )
    """,
    
    "ems_units": """
        CREATE TABLE ems_units (
            unit_id VARCHAR(20) PRIMARY KEY,
            unit_number VARCHAR(20) NOT NULL,
            unit_type VARCHAR(20) NOT NULL,
            unit_name VARCHAR(100) NOT NULL,
            crew_size INT NOT NULL,
            vehicle_type VARCHAR(50) NOT NULL,
            vehicle_year INT NOT NULL,
            mileage INT NOT NULL,
            station VARCHAR(100) NOT NULL,
            station_address VARCHAR(200) NOT NULL,
            current_lat DECIMAL(10, 6) NOT NULL,
            current_lng DECIMAL(10, 6) NOT NULL,
            status VARCHAR(50) NOT NULL,
            is_available BIT DEFAULT 1,
            current_incident VARCHAR(20),
            destination VARCHAR(200),
            estimated_arrival DATETIME2,
            last_incident_time DATETIME2,
            created_timestamp DATETIME2 DEFAULT GETDATE()
        )
    """,
    
    "hospitals": """
        CREATE TABLE hospitals (
            hospital_id VARCHAR(20) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            hospital_type VARCHAR(20) NOT NULL,
            level VARCHAR(20) NOT NULL,
            address VARCHAR(200) NOT NULL,
            lat DECIMAL(10, 6) NOT NULL,
            lng DECIMAL(10, 6) NOT NULL,
            total_capacity INT NOT NULL,
            current_capacity INT NOT NULL,
            available_beds INT NOT NULL,
            ed_status VARCHAR(20) NOT NULL,
            average_wait_time INT NOT NULL,
            trauma_level VARCHAR(20) NOT NULL,
            helicopter_pad BIT DEFAULT 0,
            burn_unit BIT DEFAULT 0,
            stroke_center BIT DEFAULT 0,
            created_timestamp DATETIME2 DEFAULT GETDATE()
        )
    """,
    
    "provider_notes": """
        CREATE TABLE provider_notes (
            note_id VARCHAR(20) PRIMARY KEY,
            incident_id VARCHAR(20) NOT NULL,
            crew_id VARCHAR(20) NOT NULL,
            note_type VARCHAR(20) NOT NULL,
            note_category VARCHAR(50) NOT NULL,
            content TEXT NOT NULL,
            priority VARCHAR(20) NOT NULL,
            timestamp DATETIME2 NOT NULL,
            is_urgent BIT DEFAULT 0,
            requires_followup BIT DEFAULT 0,
            created_timestamp DATETIME2 DEFAULT GETDATE(),
            FOREIGN KEY (incident_id) REFERENCES incidents(incident_id),
            FOREIGN KEY (crew_id) REFERENCES crew_members(crew_id)
        )
    """,
    
    "unit_crew_assignments": """
        CREATE TABLE unit_crew_assignments (
            assignment_id VARCHAR(20) PRIMARY KEY,
            unit_id VARCHAR(20) NOT NULL,
            crew_id VARCHAR(20) NOT NULL,
            assignment_date DATE NOT NULL,
            shift_start TIME,
            shift_end TIME,
            is_active BIT DEFAULT 1,
            created_timestamp DATETIME2 DEFAULT GETDATE(),
            FOREIGN KEY (unit_id) REFERENCES ems_units(unit_id),
            FOREIGN KEY (crew_id) REFERENCES crew_members(crew_id)
        )
    """,
    
    "hospital_specialties": """
        CREATE TABLE hospital_specialties (
            specialty_id VARCHAR(20) PRIMARY KEY,
            hospital_id VARCHAR(20) NOT NULL,
            specialty_name VARCHAR(100) NOT NULL,
            created_timestamp DATETIME2 DEFAULT GETDATE(),
            FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id)
        )
    """,
    
    "response_logs": """
        CREATE TABLE response_logs (
            log_id VARCHAR(20) PRIMARY KEY,
            incident_id VARCHAR(20) NOT NULL,
            unit_id VARCHAR(20) NOT NULL,
            status VARCHAR(50) NOT NULL,
            timestamp DATETIME2 NOT NULL,
            location_lat DECIMAL(10, 6),
            location_lng DECIMAL(10, 6),
            notes TEXT,
            created_timestamp DATETIME2 DEFAULT GETDATE(),
            FOREIGN KEY (incident_id) REFERENCES incidents(incident_id),
            FOREIGN KEY (unit_id) REFERENCES ems_units(unit_id)
        )
    """,
    
    "performance_metrics": """
        CREATE TABLE performance_metrics (
            metric_id VARCHAR(20) PRIMARY KEY,
            incident_id VARCHAR(20) NOT NULL,
            response_time_minutes INT,
            scene_time_minutes INT,
            transport_time_minutes INT,
            total_time_minutes INT,
            created_timestamp DATETIME2 DEFAULT GETDATE(),
            FOREIGN KEY (incident_id) REFERENCES incidents(incident_id)
        )
    """
}

# MongoDB Schema - Document Database
MONGODB_SCHEMA = {
    # Existing collections
    "incident_details": {
        "description": "Detailed incident information with medical data",
        "indexes": [
            {"field": "incident_id", "type": 1},
            {"field": "emergency_type", "type": 1},
            {"field": "priority", "type": 1},
            {"field": "timestamp", "type": -1}
        ],
        "example_document": {
            "incident_id": "INC12345",
            "caller_info": {
                "name": "John Doe",
                "age": 45,
                "sex": "Male",
                "phone": "555-1234",
                "medical_history": "Diabetes Type 2"
            },
            "location": {
                "address": "123 Main St, Richmond, VA",
                "coordinates": {"latitude": 37.5407, "longitude": -77.4348}
            },
            "emergency_type": "Heart attack symptoms",
            "priority": 1,
            "operator_notes": "Patient reports chest pain radiating to left arm",
            "symptoms": ["Chest pain", "Shortness of breath", "Sweating"],
            "vital_signs": {
                "blood_pressure": "140/90",
                "heart_rate": 95,
                "respiratory_rate": 18,
                "temperature": 98.6,
                "oxygen_saturation": 96
            },
            "patient_condition": {
                "mental_status": "Alert",
                "pain_level": 8,
                "consciousness": "Conscious",
                "breathing": "Normal",
                "circulation": "Normal"
            },
            "assigned_unit": "ALS001",
            "destination_hospital": "VCU Medical Center",
            "timestamp": "2024-01-15T10:30:00Z",
            "status": "dispatched"
        }
    },
    
    # New collections for expanded simulation
    "crew_details": {
        "description": "Detailed crew member information and schedules",
        "indexes": [
            {"field": "crew_id", "type": 1},
            {"field": "is_active", "type": 1},
            {"field": "certification", "type": 1},
            {"field": "assigned_unit", "type": 1}
        ],
        "example_document": {
            "crew_id": "CREW12345",
            "name": "Sarah Johnson",
            "age": 32,
            "sex": "Female",
            "certification": "EMT-Paramedic",
            "role": "Paramedic",
            "department": "Richmond Fire Department",
            "years_experience": 8,
            "hire_date": "2016-03-15T00:00:00Z",
            "phone": "555-9876",
            "email": "sarah.johnson@rfd.gov",
            "is_active": True,
            "current_shift": "Day Shift (06:00-18:00)",
            "assigned_unit": "ALS001",
            "schedules": [
                {
                    "date": "2024-01-15",
                    "shift_type": "Day Shift (06:00-18:00)",
                    "start_time": "06:00",
                    "end_time": "18:00",
                    "is_working": True
                }
            ],
            "certifications": ["EMT-Paramedic", "ACLS", "PALS", "PHTLS"],
            "created_timestamp": "2024-01-15T08:00:00Z"
        }
    },
    
    "unit_status_streams": {
        "description": "Real-time unit status and location updates",
        "indexes": [
            {"field": "unit_id", "type": 1},
            {"field": "status", "type": 1},
            {"field": "is_available", "type": 1},
            {"field": "timestamp", "type": -1}
        ],
        "example_document": {
            "unit_id": "ALS001",
            "unit_number": "ALS-001",
            "unit_type": "ALS",
            "unit_name": "Advanced Life Support",
            "crew_size": 2,
            "capabilities": ["IV Therapy", "Cardiac Monitoring", "Advanced Airway", "Medication Administration"],
            "vehicle_type": "Type I Ambulance",
            "vehicle_year": 2022,
            "mileage": 45000,
            "station": "Station 1 - Downtown",
            "station_address": "100 N 7th St, Richmond, VA 23219",
            "current_location": {
                "latitude": 37.5407,
                "longitude": -77.4348
            },
            "status": "En Route",
            "is_available": False,
            "assigned_crew": ["CREW12345", "CREW12346"],
            "current_incident": "INC12345",
            "destination": "123 Main St, Richmond, VA",
            "estimated_arrival": "2024-01-15T10:35:00Z",
            "last_incident_time": "2024-01-15T09:45:00Z",
            "status_history": [
                {
                    "status": "Available",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "location": {"latitude": 37.5407, "longitude": -77.4348}
                },
                {
                    "status": "En Route",
                    "timestamp": "2024-01-15T10:32:00Z",
                    "location": {"latitude": 37.5410, "longitude": -77.4350}
                }
            ],
            "created_timestamp": "2024-01-15T08:00:00Z"
        }
    },
    
    "hospital_status": {
        "description": "Hospital capacity and status information",
        "indexes": [
            {"field": "hospital_id", "type": 1},
            {"field": "hospital_type", "type": 1},
            {"field": "ed_status", "type": 1},
            {"field": "available_beds", "type": 1}
        ],
        "example_document": {
            "hospital_id": "HOSP12345",
            "name": "VCU Medical Center",
            "hospital_type": "TRAUMA",
            "level": "Level I",
            "specialties": ["Trauma Surgery", "Emergency Medicine", "Orthopedics", "Neurosurgery"],
            "address": "1200 E Broad St, Richmond, VA 23219",
            "coordinates": {"latitude": 37.5407, "longitude": -77.4348},
            "total_capacity": 400,
            "current_capacity": 320,
            "available_beds": 80,
            "ed_status": "Open",
            "average_wait_time": 45,
            "trauma_level": "Level I",
            "helicopter_pad": True,
            "burn_unit": True,
            "stroke_center": True,
            "capacity_history": [
                {
                    "timestamp": "2024-01-15T10:00:00Z",
                    "current_capacity": 315,
                    "available_beds": 85,
                    "ed_status": "Open"
                },
                {
                    "timestamp": "2024-01-15T10:30:00Z",
                    "current_capacity": 320,
                    "available_beds": 80,
                    "ed_status": "Open"
                }
            ],
            "created_timestamp": "2024-01-15T08:00:00Z"
        }
    },
    
    "provider_notes": {
        "description": "Field provider notes and medical reports",
        "indexes": [
            {"field": "note_id", "type": 1},
            {"field": "incident_id", "type": 1},
            {"field": "crew_id", "type": 1},
            {"field": "note_type", "type": 1},
            {"field": "is_urgent", "type": 1},
            {"field": "timestamp", "type": -1}
        ],
        "example_document": {
            "note_id": "NOTE12345",
            "incident_id": "INC12345",
            "crew_id": "CREW12345",
            "note_type": "ASSESSMENT",
            "note_category": "Patient Assessment",
            "content": "Patient stable. Vital signs: BP 140/90, HR 95, RR 18, O2 96%.",
            "priority": "Medium",
            "timestamp": "2024-01-15T10:35:00Z",
            "is_urgent": False,
            "requires_followup": False,
            "medical_context": {
                "vital_signs": {
                    "blood_pressure": "140/90",
                    "heart_rate": 95,
                    "respiratory_rate": 18,
                    "oxygen_saturation": 96
                },
                "assessment_findings": "Patient alert and oriented, no obvious trauma"
            },
            "created_timestamp": "2024-01-15T10:35:00Z"
        }
    },
    
    "incident_reports": {
        "description": "Comprehensive incident reports with narrative sections",
        "indexes": [
            {"field": "report_id", "type": 1},
            {"field": "incident_id", "type": 1},
            {"field": "crew_id", "type": 1},
            {"field": "is_complete", "type": 1},
            {"field": "timestamp", "type": -1}
        ],
        "example_document": {
            "report_id": "REPORT12345",
            "incident_id": "INC12345",
            "crew_id": "CREW12345",
            "report_type": "COMPREHENSIVE",
            "narrative": "Unit dispatched to 123 Main St for heart attack symptoms. Upon arrival, patient was found in stable condition.",
            "assessment": "Primary survey revealed patent airway, adequate breathing, and present circulation. Secondary survey showed no additional injuries.",
            "treatment": "Treatment included oxygen therapy and cardiac monitoring. Patient responded well to interventions.",
            "outcome": "Patient transported to VCU Medical Center in stable condition. Handoff completed without complications.",
            "timestamp": "2024-01-15T11:30:00Z",
            "is_complete": True,
            "requires_review": False,
            "attachments": [],
            "created_timestamp": "2024-01-15T11:30:00Z"
        }
    },
    
    "performance_analytics": {
        "description": "Analytics and performance metrics for incidents and units",
        "indexes": [
            {"field": "incident_id", "type": 1},
            {"field": "unit_id", "type": 1},
            {"field": "date", "type": 1},
            {"field": "response_time", "type": 1}
        ],
        "example_document": {
            "incident_id": "INC12345",
            "unit_id": "ALS001",
            "date": "2024-01-15",
            "response_time_minutes": 5,
            "scene_time_minutes": 15,
            "transport_time_minutes": 12,
            "total_time_minutes": 32,
            "performance_metrics": {
                "response_time_category": "Excellent (< 6 minutes)",
                "scene_efficiency": "Good",
                "transport_efficiency": "Good",
                "overall_performance": "Good"
            },
            "quality_indicators": {
                "protocols_followed": True,
                "documentation_complete": True,
                "patient_outcome": "Positive",
                "safety_incidents": 0
            },
            "created_timestamp": "2024-01-15T11:30:00Z"
        }
    }
}

# Index definitions for SQL Server
SQL_INDEXES = [
    # Incidents table indexes
    "CREATE INDEX idx_incidents_emergency_type ON incidents(emergency_type)",
    "CREATE INDEX idx_incidents_priority ON incidents(priority)",
    "CREATE INDEX idx_incidents_status ON incidents(status)",
    "CREATE INDEX idx_incidents_timestamp ON incidents(call_timestamp)",
    "CREATE INDEX idx_incidents_assigned_unit ON incidents(assigned_unit)",
    
    # Crew members table indexes
    "CREATE INDEX idx_crew_active ON crew_members(is_active)",
    "CREATE INDEX idx_crew_certification ON crew_members(certification)",
    "CREATE INDEX idx_crew_assigned_unit ON crew_members(assigned_unit)",
    "CREATE INDEX idx_crew_department ON crew_members(department)",
    
    # EMS units table indexes
    "CREATE INDEX idx_units_type ON ems_units(unit_type)",
    "CREATE INDEX idx_units_status ON ems_units(status)",
    "CREATE INDEX idx_units_available ON ems_units(is_available)",
    "CREATE INDEX idx_units_station ON ems_units(station)",
    
    # Hospitals table indexes
    "CREATE INDEX idx_hospitals_type ON hospitals(hospital_type)",
    "CREATE INDEX idx_hospitals_status ON hospitals(ed_status)",
    "CREATE INDEX idx_hospitals_capacity ON hospitals(available_beds)",
    "CREATE INDEX idx_hospitals_location ON hospitals(lat, lng)",
    
    # Provider notes table indexes
    "CREATE INDEX idx_notes_incident ON provider_notes(incident_id)",
    "CREATE INDEX idx_notes_crew ON provider_notes(crew_id)",
    "CREATE INDEX idx_notes_type ON provider_notes(note_type)",
    "CREATE INDEX idx_notes_urgent ON provider_notes(is_urgent)",
    "CREATE INDEX idx_notes_timestamp ON provider_notes(timestamp)",
    
    # Response logs table indexes
    "CREATE INDEX idx_logs_incident ON response_logs(incident_id)",
    "CREATE INDEX idx_logs_unit ON response_logs(unit_id)",
    "CREATE INDEX idx_logs_status ON response_logs(status)",
    "CREATE INDEX idx_logs_timestamp ON response_logs(timestamp)",
    
    # Performance metrics table indexes
    "CREATE INDEX idx_metrics_incident ON performance_metrics(incident_id)",
    "CREATE INDEX idx_metrics_response_time ON performance_metrics(response_time_minutes)"
]

def get_sql_schema():
    """Get the complete SQL Server schema"""
    return SQL_SCHEMA

def get_mongodb_schema():
    """Get the complete MongoDB schema"""
    return MONGODB_SCHEMA

def get_sql_indexes():
    """Get the SQL Server indexes"""
    return SQL_INDEXES

def print_schema_summary():
    """Print a summary of the database schemas"""
    print("🗄️ === DATABASE SCHEMA SUMMARY ===")
    
    print("\n📊 SQL Server Tables:")
    for table_name in SQL_SCHEMA.keys():
        print(f"   ✅ {table_name}")
    
    print("\n📄 MongoDB Collections:")
    for collection_name in MONGODB_SCHEMA.keys():
        print(f"   ✅ {collection_name}")
    
    print(f"\n🔍 SQL Indexes: {len(SQL_INDEXES)} indexes defined")
    
    print("\n📋 Schema Features:")
    print("   • Complete incident tracking with medical data")
    print("   • Crew management and scheduling")
    print("   • Unit status and location tracking")
    print("   • Hospital capacity and specialty management")
    print("   • Provider notes and medical reports")
    print("   • Performance analytics and metrics")
    print("   • Real-time status updates")
    print("   • Comprehensive indexing for performance")

if __name__ == "__main__":
    print_schema_summary()