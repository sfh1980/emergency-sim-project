"""
Data Adapter for Emergency Services Simulation Platform

Converts data generator output to the format expected by the unified data saver.
Handles field name mismatches and data structure differences.
"""

from datetime import datetime


class DataAdapter:
    """Adapter to convert data generator output to unified data saver format"""
    
    @staticmethod
    def adapt_crew_data(crew_data):
        """Convert crew generator output to unified saver format"""
        # Shorten phone number to avoid truncation
        phone = crew_data.get('phone', '')
        if len(phone) > 15:  # Limit to 15 characters
            phone = phone[:15]
        
        return {
            'crew_id': crew_data['crew_id'],
            'first_name': crew_data['name'].split()[0] if 'name' in crew_data else 'Unknown',
            'last_name': crew_data['name'].split()[-1] if 'name' in crew_data and len(crew_data['name'].split()) > 1 else 'Unknown',
            'certification_level': crew_data.get('certification', 'Unknown'),
            'years_experience': crew_data.get('years_experience', 0),
            'is_active': crew_data.get('is_active', True),
            'hire_date': crew_data.get('hire_date', datetime.now()),
            'phone_number': phone,
            'email': crew_data.get('email', ''),
            'emergency_contact': f"{crew_data.get('name', 'Unknown')} - {phone}",
            'certifications': crew_data.get('certification', 'Unknown'),
            'specializations': crew_data.get('role', 'Unknown'),
            'assigned_unit': crew_data.get('assigned_unit'),
            'current_shift': crew_data.get('current_shift'),
            'last_incident': None,
            'total_incidents': 0,
            'response_time_avg': 0,
            'patient_satisfaction': 0
        }
    
    @staticmethod
    def adapt_unit_data(unit_data):
        """Convert unit generator output to unified saver format"""
        # Create a shorter unit number to avoid truncation
        unit_type = unit_data.get('unit_type', 'UNK')
        unit_id_suffix = unit_data['unit_id'][-1]
        
        # For longer unit types, use just the first letter and suffix
        if len(unit_type) > 3:
            unit_number = f"{unit_type[0]}{unit_id_suffix}"
        else:
            unit_number = f"{unit_type[:2]}{unit_id_suffix}"
        
        # Ensure unit number doesn't exceed 10 characters
        if len(unit_number) > 10:
            unit_number = unit_number[:10]
        
        return {
            'unit_id': unit_data['unit_id'],
            'unit_number': unit_data.get('unit_number', unit_number),
            'unit_name': unit_data.get('unit_name', unit_data['unit_id']),
            'unit_type': unit_data.get('unit_type', 'Unknown'),
            'vehicle_type': unit_data.get('vehicle_type', 'Ambulance'),
            'vehicle_year': unit_data.get('vehicle_year', 2020),
            'mileage': unit_data.get('mileage', 50000),
            'station': unit_data.get('station', 'Main Station'),
            'station_address': unit_data.get('station_address', '123 Main St'),
            'current_lat': unit_data.get('current_location', {}).get('latitude', 37.5407),
            'current_lng': unit_data.get('current_location', {}).get('longitude', -77.4348),
            'status': unit_data.get('status', 'Available'),
            'is_available': unit_data.get('is_available', True),
            'current_incident': unit_data.get('current_incident'),
            'destination': unit_data.get('destination'),
            'estimated_arrival': unit_data.get('estimated_arrival'),
            'last_incident_time': unit_data.get('last_incident_time')
        }
    
    @staticmethod
    def adapt_hospital_data(hospital_data):
        """Convert hospital generator output to unified saver format"""
        return {
            'hospital_id': hospital_data['hospital_id'],
            'hospital_name': hospital_data.get('name', hospital_data['hospital_id']),
            'address': hospital_data.get('address', 'Unknown Address'),
            'phone_number': hospital_data.get('phone', ''),
            'hospital_type': hospital_data.get('hospital_type', 'General'),
            'level': hospital_data.get('level', 'Level I'),
            'total_capacity': hospital_data.get('total_capacity', 100),
            'current_capacity': hospital_data.get('current_capacity', 75),
            'available_beds': hospital_data.get('available_beds', 25),
            'ed_status': hospital_data.get('ed_status', 'Open'),
            'average_wait_time': hospital_data.get('average_wait_time', 30),
            'trauma_level': hospital_data.get('trauma_level', 'Level I'),
            'helicopter_pad': hospital_data.get('helicopter_pad', False),
            'burn_unit': hospital_data.get('burn_unit', False),
            'stroke_center': hospital_data.get('stroke_center', False),
            'lat': hospital_data.get('location', {}).get('coordinates', {}).get('latitude', 37.5407),
            'lng': hospital_data.get('location', {}).get('coordinates', {}).get('longitude', -77.4348)
        }
    
    @staticmethod
    def adapt_provider_note_data(note_data):
        """Convert provider notes generator output to unified saver format"""
        return {
            'note_id': note_data['note_id'],
            'incident_id': note_data.get('incident_id', 'INC_UNKNOWN'),
            'crew_id': note_data.get('crew_id', 'CREW_UNKNOWN'),
            'note_type': note_data.get('note_type', 'General'),
            'note_content': note_data.get('content', note_data.get('note_content', 'No content')),
            'is_urgent': note_data.get('is_urgent', False),
            'timestamp': note_data.get('timestamp', datetime.now()),
            'created_by': note_data.get('created_by', 'Unknown Provider')
        }
    
    @staticmethod
    def adapt_incident_data(incident_data):
        """Convert incident generator output to unified saver format"""
        # Incident data is already in the correct format
        return incident_data
