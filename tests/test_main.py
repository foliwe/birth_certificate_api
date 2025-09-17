import pytest
from datetime import date

def test_app_startup(client):
    """Test that the application starts up correctly"""
    response = client.get("/docs")
    assert response.status_code == 200

def test_get_nonexistent_certificate(client):
    """Test getting a certificate that doesn't exist"""
    response = client.get("/birth-certificate/INVALID123")
    assert response.status_code == 404
    assert "Birth certificate not found" in response.json()["detail"]

def test_create_birth_certificate(client):
    """Test creating a new birth certificate"""
    birth_certificate_data = {
        "certificate_info": {
            "title": "Birth Certificate",
            "registration_number": "BC12345678",
            "date_of_issue": "2023-01-15",
            "issuing_authority": "Municipal Corporation",
            "registrar_name": "Chief Registrar John Doe"
        },
        "child_info": {
            "name": "Jane Doe",
            "date_of_birth": "2023-01-01",
            "place_of_birth": "City Hospital",
            "sex": "Female"
        },
        "father_info": {
            "name": "John Doe",
            "nationality": "American",
            "profession": "Engineer",
            "residence": "123 Main St",
            "date_of_birth": "1990-01-01",
            "place_of_birth": "New York"
        },
        "mother_info": {
            "name": "Jane Smith",
            "nationality": "American",
            "profession": "Doctor",
            "residence": "123 Main St",
            "date_of_birth": "1992-01-01",
            "place_of_birth": "Boston"
        }
    }
    
    response = client.post("/birth-certificate/", json=birth_certificate_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["certificate_info"]["registration_number"] == "BC12345678"
    assert data["child_info"]["name"] == "Jane Doe"
    assert data["father_info"]["name"] == "John Doe"
    assert data["mother_info"]["name"] == "Jane Smith"

def test_get_existing_certificate(client):
    """Test retrieving an existing certificate"""
    # First create a certificate
    birth_certificate_data = {
        "certificate_info": {
            "title": "Birth Certificate",
            "registration_number": "BC87654321",
            "date_of_issue": "2023-02-15",
            "issuing_authority": "City Corporation",
            "registrar_name": "Deputy Registrar Mary Smith"
        },
        "child_info": {
            "name": "Bob Johnson",
            "date_of_birth": "2023-02-01",
            "place_of_birth": "General Hospital",
            "sex": "Male"
        },
        "father_info": {
            "name": "Robert Johnson",
            "nationality": "Canadian",
            "profession": "Teacher",
            "residence": "456 Oak Ave",
            "date_of_birth": "1988-01-01",
            "place_of_birth": "Toronto"
        },
        "mother_info": {
            "name": "Alice Brown",
            "nationality": "Canadian",
            "profession": "Nurse",
            "residence": "456 Oak Ave",
            "date_of_birth": "1990-01-01",
            "place_of_birth": "Vancouver"
        }
    }
    
    # Create the certificate
    create_response = client.post("/birth-certificate/", json=birth_certificate_data)
    assert create_response.status_code == 200
    
    # Retrieve the certificate
    get_response = client.get("/birth-certificate/BC87654321")
    assert get_response.status_code == 200
    
    data = get_response.json()
    assert data["certificate_info"]["registration_number"] == "BC87654321"
    assert data["child_info"]["name"] == "Bob Johnson"

def test_list_certificates(client):
    """Test listing certificates with pagination"""
    response = client.get("/birth-certificates/?page=1&limit=5")
    assert response.status_code == 200
    
    data = response.json()
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    assert "data" in data
    assert data["page"] == 1
    assert data["limit"] == 5