from faker import Faker
import random
from datetime import datetime


RICHMOND_STREETS = [
    "Main Street", "Cary Street", "Broad Street", "Monument Avenue",
    "Lombardy Street", "Grace Street", "Franklin Street", "Marshall Street",
    "Clay Street", "Leigh Street", "Chamberlayne Avenue", "Patterson Avenue",
    "Hull Street", "Midlothian Turnpike", "Forest Hill Avenue", "Semmes Avenue",
    "Grove Avenue", "Staples Mill Road", "Parham Road", "Three Chopt Road"
]

RICHMOND_AREAS = [
    "Fan District", "Museum District", "Carytown", "Shockoe Bottom",
    "Church Hill", "Jackson Ward", "Oregon Hill", "West End",
    "North Side", "South Side", "East End", "Westover Hills",
    "Bellevue", "Ginter Park", "Lakeside", "Bon Air"
]

RICHMOND_ZIP_CODES = [
    "23219", "23220", "23221", "23222", "23223", "23224", "23225", "23226",
    "23227", "23228", "23229", "23230", "23231", "23232", "23233", "23234",
    "23235", "23236", "23237", "23238", "23239", "23240", "23241", "23242"
]

def generate_richmond_address():
    """Generate a realistic Richmond, VA address"""
    street_number = random.randint(100, 9999)
    street = random.choice(RICHMOND_STREETS)
    area = random.choice(RICHMOND_AREAS)
    zip_code = random.choice(RICHMOND_ZIP_CODES)
    
    return f"{street_number} {street}, {area}, Richmond, VA {zip_code}"

# Create data lists
MEDICAL_EMERGENCIES = [
    "Cardiac Arrest", "Heart Attack Symptoms", "Stroke Symptoms", "Respiratory Symptoms",
    "Diabetic Emergency", "Seizure Emergency",
    "Unconscious/Unresponsive", "Mental Health Crisis",
    "Pediatric Emergency", "DOA", "Severe Bleeding",
    "Allergic Reactions", "Overdose/Poisoning", "Heat Stroke",
    "Hypothermia", "Childbirth/Labor", "Fall (Elderly)"
]

NON_MEDICAL_EMERGENCIES = [
    "Car Accident With Injuries", "Car Accident Without Injuries",
    "Mass Casualty Event", "Shooting Incident",
    "Fall (Construction)", "Drowning", "Near Drowning",
    "Fire-related Incident", "Non-Emergency Transport", "Trauma", "Sports Injury"
]

MEDICAL_CONDITIONS = [
    "Diabetes Type 1", "Diabetes Type 2", "Hypertension", "Asthma",
    "Heart disease", "COPD", "Epilepsy", "Cancer", "Kidney disease",
    "Liver disease", "Arthritis", "Depression", "Anxiety",
    "Bipolar disorder", "Schizophrenia", "Alzheimer's", "Dementia",
    "Parkinson's disease", "Multiple sclerosis", "Lupus",
    "Rheumatoid arthritis", "Thyroid disorders", "Sleep apnea",
    "Obesity", "Anemia", "Blood clotting disorders", "None"
]

# Create a Faker instance
fake = Faker()

# Test the Faker instance
def test_data_generation():
    print("=== TESTING DATA GENERATION ===")
    print(f"Random medical emergency: {random.choice(MEDICAL_EMERGENCIES)}")
    print(f"Random medical condition: {random.choice(MEDICAL_CONDITIONS)}")
    print(f"Richmond address: {generate_richmond_address()}")
    print(f"Fake name: {fake.name()}")
    print(f"Random age: {fake.random_int(min=18, max=95)}")

if __name__ == "__main__":
    test_data_generation()