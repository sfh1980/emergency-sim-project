"""
Dashboard for Emergency Services Mock App
Simple web interface to display incident data
"""

from flask import Flask, render_template, jsonify
import pyodbc
import pymongo
from datetime import datetime
import json

app = Flask(__name__)

class DashboardData:
    def __init__(self):
        self.sql_connection = None
        self.mongo_client = None
        self.mongo_db = None
        self.connect_databases()
    
    def connect_databases(self):
        """Connect to both databases"""
        # SQL Server connection
        self.sql_connection = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"
            "DATABASE=EmergencyMock;"
            "Trusted_Connection=yes;"
        )
        
        # MongoDB connection
        self.mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mongo_db = self.mongo_client["EmergencyMock"]
    
    def get_recent_incidents(self, limit=10):
        """Get recent incidents from SQL Server"""
        cursor = self.sql_connection.cursor()
        cursor.execute("""
            SELECT TOP (?) incident_id, caller_name, emergency_type, 
                   priority, status, call_timestamp
            FROM incidents 
            ORDER BY call_timestamp DESC
        """, limit)
        
        incidents = []
        for row in cursor.fetchall():
            incidents.append({
                'id': row[0],
                'caller': row[1],
                'type': row[2],
                'priority': row[3],
                'status': row[4],
                'timestamp': row[5].isoformat() if row[5] else None
            })
        
        return incidents
    
    def get_incident_details(self, incident_id):
        """Get detailed incident info from MongoDB"""
        collection = self.mongo_db["incident_details"]
        incident = collection.find_one({"incident_id": incident_id})
        
        if incident:
            # Convert ObjectId to string for JSON serialization
            incident['_id'] = str(incident['_id'])
        
        return incident

# Create global dashboard data instance
dashboard_data = DashboardData()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/incidents')
def get_incidents():
    """API endpoint to get recent incidents"""
    incidents = dashboard_data.get_recent_incidents(20)
    return jsonify(incidents)

@app.route('/api/incident/<incident_id>')
def get_incident_details(incident_id):
    """API endpoint to get detailed incident info"""
    details = dashboard_data.get_incident_details(incident_id)
    return jsonify(details)

if __name__ == '__main__':
    print("🚨 Starting Emergency Services Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)