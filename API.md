# API Documentation

## Birth Certificate Registration API

This document provides detailed information about the API endpoints available in the Birth Certificate Registration system.

### Base URL
```
http://localhost:8000
```

### Authentication
Currently, no authentication is required for API access.

## Endpoints

### 1. Create Birth Certificate

**Endpoint:** `POST /birth-certificate/`

**Description:** Creates a new birth certificate record in the system.

**Request Body:**
```json
{
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
```

**Response:** 
- **Status 200:** Returns the created birth certificate object
- **Status 422:** Validation error

### 2. Get Birth Certificate

**Endpoint:** `GET /birth-certificate/{registration_number}`

**Description:** Retrieves a specific birth certificate by its registration number.

**Path Parameters:**
- `registration_number` (string): The unique registration number of the birth certificate

**Response:**
- **Status 200:** Returns the birth certificate object
- **Status 404:** Birth certificate not found

**Example:**
```
GET /birth-certificate/BC12345678
```

### 3. List Birth Certificates

**Endpoint:** `GET /birth-certificates/`

**Description:** Retrieves a paginated list of all birth certificates.

**Query Parameters:**
- `page` (integer, optional): Page number (default: 1, minimum: 1)
- `limit` (integer, optional): Number of items per page (default: 10, minimum: 1, maximum: 100)

**Response:**
- **Status 200:** Returns paginated birth certificates

**Example:**
```
GET /birth-certificates/?page=1&limit=10
```

**Response Format:**
```json
{
  "total": 25,
  "page": 1,
  "limit": 10,
  "data": [
    {
      "certificate_info": { ... },
      "child_info": { ... },
      "father_info": { ... },
      "mother_info": { ... }
    }
  ]
}
```

## Data Models

### CertificateInformation
- `title` (string): Certificate title
- `registration_number` (string): Unique registration number
- `date_of_issue` (date): Date when the certificate was issued
- `issuing_authority` (string): Authority that issued the certificate
- `registrar_name` (string): Name of the registrar

### ChildInformation
- `name` (string): Full name of the child
- `date_of_birth` (date, optional): Child's date of birth
- `place_of_birth` (string): Place where the child was born
- `sex` (string): Child's sex/gender

### ParentInformation
- `name` (string): Full name of the parent
- `nationality` (string): Parent's nationality
- `profession` (string): Parent's profession
- `residence` (string): Parent's residential address
- `date_of_birth` (date, optional): Parent's date of birth
- `place_of_birth` (string): Parent's place of birth

### BirthCertificate
- `certificate_info` (CertificateInformation): Certificate details
- `child_info` (ChildInformation): Child details
- `father_info` (ParentInformation): Father's details
- `mother_info` (ParentInformation): Mother's details

## Error Responses

### 404 Not Found
```json
{
  "detail": "Birth certificate not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Database error: [error message]"
}
```

## Interactive Documentation

The API provides interactive documentation at:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

These interfaces allow you to test the API endpoints directly from your browser.