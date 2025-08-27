"""
Emergency Services Data Generators Package

This package contains specialized generators for creating realistic
emergency services simulation data including incidents, crew, units,
hospitals, and provider notes.

Modules:
    - base_generator: Base class with common functionality
    - incident_generator: Emergency call generation
    - crew_generator: Personnel and shift management
    - unit_generator: EMS unit management
    - hospital_generator: Hospital data and specialties
    - provider_notes_generator: Field updates and reports
    - master_generator: Coordinates all generators
"""

from .base_generator import BaseGenerator
from .incident_generator import IncidentGenerator
from .crew_generator import CrewGenerator
from .unit_generator import UnitGenerator
from .hospital_generator import HospitalGenerator
from .provider_notes_generator import ProviderNotesGenerator
from .master_generator import MasterGenerator

__all__ = [
    'BaseGenerator',
    'IncidentGenerator', 
    'CrewGenerator',
    'UnitGenerator',
    'HospitalGenerator',
    'ProviderNotesGenerator',
    'MasterGenerator'
]
