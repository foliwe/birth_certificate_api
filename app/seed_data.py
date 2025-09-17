from faker import Faker
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import sys
import os

# Add the parent directory to the path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, engine
from models import database_models
from models.database_models import Base

# Create all tables
Base.metadata.create_all(bind=engine)

fake = Faker()

# Initialize the database session
db = SessionLocal()

# List of possible values for various fields
authorities = [
    "Municipal Corporation of Delhi",
    "Greater Mumbai Municipal Corporation",
    "Bangalore City Corporation",
    "Chennai Municipal Corporation",
    "Kolkata Municipal Corporation"
]

registrar_titles = [
    "Chief Registrar",
    "Deputy Registrar",
    "Senior Registrar",
    "Assistant Registrar",
    "Principal Registrar"
]

nationalities = [
    "Indian",
    "American",
    "British",
    "Canadian",
    "Australian"
]

professions = [
    "Doctor",
    "Engineer",
    "Teacher",
    "Business Owner",
    "Lawyer",
    "Accountant",
    "Software Developer",
    "Architect",
    "Chef",
    "Police Officer"
]

def generate_registration_number():
    return f"BC{fake.unique.random_number(digits=8)}"

def generate_fake_date(start_year=1960, end_year=2025):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    return fake.date_between(start_date=start_date, end_date=end_date)

# Generate 30 birth certificates
for _ in range(30):
    # Create certificate
    cert_date = generate_fake_date(2020, 2025)
    db_certificate = database_models.Certificate(
        title="Birth Certificate",
        registration_number=generate_registration_number(),
        date_of_issue=cert_date,
        issuing_authority=random.choice(authorities),
        registrar_name=f"{random.choice(registrar_titles)} {fake.name()}"
    )
    db.add(db_certificate)
    db.flush()

    # Create child
    child_dob = cert_date - timedelta(days=random.randint(7, 90))  # Certificate issued 7-90 days after birth
    db_child = database_models.Child(
        name=fake.name(),
        date_of_birth=child_dob,
        place_of_birth=fake.city(),
        sex=random.choice(["Male", "Female"]),
        certificate_id=db_certificate.id
    )
    db.add(db_child)

    # Create father (30-50 years older than child)
    father_dob = child_dob - timedelta(days=random.randint(30*365, 50*365))
    db_father = database_models.Parent(
        name=fake.name_male(),
        nationality=random.choice(nationalities),
        profession=random.choice(professions),
        residence=f"{fake.street_address()}, {fake.city()}",
        date_of_birth=father_dob,
        place_of_birth=fake.city(),
        father_of_id=db_certificate.id
    )
    db.add(db_father)

    # Create mother (25-45 years older than child)
    mother_dob = child_dob - timedelta(days=random.randint(25*365, 45*365))
    db_mother = database_models.Parent(
        name=fake.name_female(),
        nationality=random.choice(nationalities),
        profession=random.choice(professions),
        residence=f"{fake.street_address()}, {fake.city()}",
        date_of_birth=mother_dob,
        place_of_birth=fake.city(),
        mother_of_id=db_certificate.id
    )
    db.add(db_mother)

# Commit all records to the database
db.commit()
db.close()

print("Successfully inserted 30 birth certificate records with fake data!")