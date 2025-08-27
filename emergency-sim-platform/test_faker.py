from faker import Faker

# Create a Faker instance
fake = Faker()

# Test different types of fake data
print("=== FAKER TEST RESULES ===")
print(f"Name: {fake.name()}")
print(f"Email: {fake.email()}")
print(f"Address: {fake.address()}")
print(f"Phone: {fake.phone_number()}")
print(f"Date: {fake.date_of_birth()}")
print(f"Age: {fake.random_int(min=18, max=80)}")
print(f"Medical Condition: {fake.random_element(['Heart Attack', 'Stroke', 'Fainting', 'Seizure', 'Other'])}")
