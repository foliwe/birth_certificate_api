# Birth Certificate Registration API

A FastAPI-based web application for managing birth certificate registrations with a SQLite database backend.

## Features

- Create new birth certificates with complete family information
- Retrieve birth certificates by registration number
- List all birth certificates with pagination
- SQLite database for data persistence
- RESTful API design with automatic documentation

## Project Structure

```
birth_certificate_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and endpoints
│   ├── database.py          # Database configuration and connection
│   ├── seed_data.py         # Script to populate database with sample data
│   ├── test_db.py           # Database testing utilities
│   └── models/
│       ├── __init__.py
│       ├── models.py        # Pydantic models for API
│       └── database_models.py # SQLAlchemy models for database
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore patterns
└── README.md               # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/foliwe/birth_certificate_api.git
cd birth_certificate_api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

Start the FastAPI development server:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- Application: http://localhost:8000
- Interactive API Documentation: http://localhost:8000/docs
- ReDoc Documentation: http://localhost:8000/redoc

### Seeding Sample Data

To populate the database with sample birth certificate data:
```bash
python app/seed_data.py
```

### Testing Database Connection

To test the database connection and relationships:
```bash
python app/test_db.py
```

## API Endpoints

### Create Birth Certificate
- **POST** `/birth-certificate/`
- Creates a new birth certificate record
- Request body: JSON with certificate, child, father, and mother information

### Get Birth Certificate
- **GET** `/birth-certificate/{registration_number}`
- Retrieves a specific birth certificate by registration number

### List Birth Certificates
- **GET** `/birth-certificates/`
- Lists all birth certificates with pagination
- Query parameters:
  - `page`: Page number (default: 1)
  - `limit`: Items per page (default: 10, max: 100)

## Data Models

The application manages three main entities:

1. **Certificate**: Basic certificate information (title, registration number, issue date, authority, registrar)
2. **Child**: Child information (name, date of birth, place of birth, sex)
3. **Parent**: Parent information (name, nationality, profession, residence, birth details)

## Development

### Project Dependencies

- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI applications
- **Faker**: Library for generating fake data for testing

### Database

The application uses SQLite for local development with the following tables:
- `certificates`: Main certificate records
- `children`: Child information linked to certificates
- `parents`: Parent information (both fathers and mothers) linked to certificates

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.