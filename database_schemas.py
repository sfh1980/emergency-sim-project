"""
Database Schema Definitions for Emergency Services Mock App
This file contains the SQL Server and MongoDB schema designs
"""

# SQL Server Schema Definitions
SQL_SCHEMAS = {
    "incidents": """
    CREATE TABLE incidents (
        incident_id VARCHAR(8) PRIMARY KEY,
        caller_name VARCHAR(100) NOT NULL,
        caller_age INT,
        caller_sex VARCHAR(10),
        location_address VARCHAR(200),
        location_lat DECIMAL(10, 8),
        location_lng DECIMAL(11, 8),
        emergency_type VARCHAR(100) NOT NULL,
        priority INT CHECK (priority BETWEEN 1 AND 5),
        status VARCHAR(50) DEFAULT 'dispatched',
        call_timestamp DATETIME2 DEFAULT GETDATE(),
        created_at DATETIME2 DEFAULT GETDATE(),
        updated_at DATETIME2 DEFAULT GETDATE()
    );
    """,
    
    "ems_units": """
    CREATE TABLE ems_units (
        unit_id VARCHAR(10) PRIMARY KEY,
        unit_type VARCHAR(20) NOT NULL, -- BLS, ALS, Supervisor
        unit_number VARCHAR(10) UNIQUE,
        current_status VARCHAR(20) DEFAULT 'available', -- available, busy, out_of_service
        current_lat DECIMAL(10, 8),
        current_lng DECIMAL(11, 8),
        home_base VARCHAR(100),
        crew_size INT DEFAULT 2,
        created_at DATETIME2 DEFAULT GETDATE()
    );
    """,
    
    "hospitals": """
    CREATE TABLE hospitals (
        hospital_id INT PRIMARY KEY IDENTITY(1,1),
        hospital_name VARCHAR(100) NOT NULL,
        address VARCHAR(200),
        lat DECIMAL(10, 8),
        lng DECIMAL(11, 8),
        specialties TEXT, -- JSON string of specialties
        current_wait_time INT DEFAULT 0, -- minutes
        bed_capacity INT,
        trauma_level INT, -- 1-5 trauma center levels
        created_at DATETIME2 DEFAULT GETDATE()
    );
    """,
    
    "response_logs": """
    CREATE TABLE response_logs (
        log_id INT PRIMARY KEY IDENTITY(1,1),
        incident_id VARCHAR(8) FOREIGN KEY REFERENCES incidents(incident_id),
        unit_id VARCHAR(10) FOREIGN KEY REFERENCES ems_units(unit_id),
        status VARCHAR(50) NOT NULL, -- dispatched, en_route, on_scene, etc.
        timestamp DATETIME2 DEFAULT GETDATE(),
        location_lat DECIMAL(10, 8),
        location_lng DECIMAL(11, 8),
        notes TEXT
    );
    """,
    
    "performance_metrics": """
    CREATE TABLE performance_metrics (
        metric_id INT PRIMARY KEY IDENTITY(1,1),
        incident_id VARCHAR(8) FOREIGN KEY REFERENCES incidents(incident_id),
        dispatch_time DATETIME2,
        response_time INT, -- seconds from dispatch to arrival
        scene_time INT, -- minutes on scene
        transport_time INT, -- minutes to hospital
        total_time INT, -- total incident duration
        hospital_id INT FOREIGN KEY REFERENCES hospitals(hospital_id),
        outcome VARCHAR(50), -- transported, treated_released, etc.
        created_at DATETIME2 DEFAULT GETDATE()
    );
    """
}

# MongoDB Schema Definitions (as Python dictionaries)
MONGO_SCHEMAS = {
    "incident_details": {
        "collection": "incident_details",
        "indexes": [
            {"incident_id": 1},
            {"emergency_type": 1},
            {"priority": 1},
            {"call_timestamp": -1}
        ],
        "example_document": {
            "incident_id": "abc12345",
            "caller_info": {
                "name": "John Doe",
                "age": 45,
                "sex": "Male",
                "phone": "555-1234",
                "medical_history": "Diabetes Type 2"
            },
            "location": {
                "address": "123 Main St, Richmond, VA",
                "coordinates": {"lat": 37.5407, "lng": -77.4348},
                "zone": "North Richmond"
            },
            "emergency_details": {
                "type": "Chest Pain",
                "priority": 2,
                "symptoms": ["Chest pain", "Shortness of breath"],
                "vital_signs": {
                    "blood_pressure": "140/90",
                    "heart_rate": 95,
                    "temperature": 98.6,
                    "oxygen_saturation": 95
                }
            },
            "patient_condition": {
                "mental_status": "Alert and oriented",
                "pain_level": "Moderate pain",
                "conscious": True
            },
            "operator_notes": "Patient reports crushing chest pain...",
            "call_timestamp": "2024-01-15T14:30:00Z",
            "created_at": "2024-01-15T14:30:00Z"
        }
    },
    
    "unit_status_streams": {
        "collection": "unit_status_streams",
        "indexes": [
            {"unit_id": 1},
            {"timestamp": -1},
            {"status": 1}
        ],
        "example_document": {
            "unit_id": "ALS001",
            "timestamp": "2024-01-15T14:35:00Z",
            "status": "en_route",
            "location": {
                "lat": 37.5407,
                "lng": -77.4348
            },
            "incident_id": "abc12345",
            "estimated_arrival": "2024-01-15T14:40:00Z"
        }
    },
    
    "provider_notes": {
        "collection": "provider_notes",
        "indexes": [
            {"incident_id": 1},
            {"provider_id": 1},
            {"timestamp": -1}
        ],
        "example_document": {
            "incident_id": "abc12345",
            "provider_id": "EMT_001",
            "timestamp": "2024-01-15T14:45:00Z",
            "note": "Patient found conscious, alert. BP 180/95, pulse 110. Administered aspirin 325mg.",
            "vital_signs": {
                "blood_pressure": "180/95",
                "heart_rate": 110,
                "temperature": 98.8
            },
            "treatments": ["Aspirin 325mg", "Oxygen therapy"]
        }
    }
}

def print_sql_schemas():
    """Print all SQL Server schemas"""
    print("=== SQL SERVER SCHEMAS ===")
    for table_name, schema in SQL_SCHEMAS.items():
        print(f"\n-- {table_name.upper()} TABLE")
        print(schema)

def print_mongo_schemas():
    """Print MongoDB schema examples"""
    print("\n=== MONGODB SCHEMAS ===")
    for collection_name, schema_info in MONGO_SCHEMAS.items():
        print(f"\n-- {collection_name.upper()} COLLECTION")
        print(f"Collection: {schema_info['collection']}")
        print("Indexes:")
        for index in schema_info['indexes']:
            print(f"  {index}")
        print("Example Document:")
        print(f"  {schema_info['example_document']}")

if __name__ == "__main__":
    print_sql_schemas()
    print_mongo_schemas()