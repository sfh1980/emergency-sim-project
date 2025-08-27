"""
Base Generator Class

Provides common functionality and structure for all data generators
in the emergency services simulation platform.
"""

import uuid
from datetime import datetime
from faker import Faker
import random


class BaseGenerator:
    """Base class for all data generators with common functionality"""
    
    def __init__(self):
        """Initialize the base generator with Faker and common utilities"""
        self.fake = Faker()
        self.generated_data = []
        
    def generate_id(self, prefix="", length=8):
        """Generate a unique ID with optional prefix"""
        unique_id = str(uuid.uuid4())[:length]
        return f"{prefix}{unique_id}" if prefix else unique_id
    
    def generate_timestamp(self, start_date=None, end_date=None):
        """Generate a realistic timestamp within a date range"""
        if start_date is None:
            start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if end_date is None:
            end_date = datetime.now()
            
        return self.fake.date_time_between(start_date=start_date, end_date=end_date)
    
    def generate_richmond_coordinates(self):
        """Generate coordinates within Richmond, VA city limits"""
        # Richmond, VA approximate boundaries
        lat_min, lat_max = 37.45, 37.65  # Latitude range
        lng_min, lng_max = -77.65, -77.35  # Longitude range
        
        return {
            'latitude': round(random.uniform(lat_min, lat_max), 6),
            'longitude': round(random.uniform(lng_min, lng_max), 6)
        }
    
    def generate_richmond_address(self):
        """Generate a realistic Richmond, VA address"""
        from incident_data import RICHMOND_STREETS, RICHMOND_AREAS, RICHMOND_ZIP_CODES
        
        street_number = random.randint(100, 9999)
        street = random.choice(RICHMOND_STREETS)
        area = random.choice(RICHMOND_AREAS)
        zip_code = random.choice(RICHMOND_ZIP_CODES)
        
        return f"{street_number} {street}, {area}, Richmond, VA {zip_code}"
    
    def add_to_generated_data(self, data_item):
        """Add generated data to the internal storage"""
        self.generated_data.append(data_item)
    
    def get_generated_data(self):
        """Return all generated data"""
        return self.generated_data
    
    def clear_generated_data(self):
        """Clear all generated data"""
        self.generated_data = []
    
    def generate_batch(self, count=1):
        """Generate a batch of data items (to be implemented by subclasses)"""
        raise NotImplementedError("Subclasses must implement generate_batch method")
    
    def validate_data(self, data_item):
        """Validate generated data (to be implemented by subclasses)"""
        raise NotImplementedError("Subclasses must implement validate_data method")
    
    def get_statistics(self):
        """Get statistics about generated data (to be implemented by subclasses)"""
        return {
            'total_generated': len(self.generated_data),
            'generator_type': self.__class__.__name__
        }
