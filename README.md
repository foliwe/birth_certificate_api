# Birth Certificate API

A FastAPI-based REST API for managing birth certificate registrations with PostgreSQL database support.

## Features

- **CRUD Operations**: Create, read, update, and delete birth certificates
- **PostgreSQL Support**: Production-ready database with SQLite fallback for development
- **Data Validation**: Comprehensive data validation using Pydantic models
- **Pagination**: Efficient pagination for listing birth certificates
- **Docker Support**: Easy deployment with Docker containers
- **Environment Configuration**: Flexible configuration using environment variables

## Project Structure

```
birth_certificate_api/
├── app/
│   ├── models/
│   │   ├── models.py           # Pydantic models for API schemas
│   │   └── database_models.py  # SQLAlchemy models for database
│   ├── database.py             # Database configuration and connection
│   ├── main.py                 # FastAPI application and routes
│   ├── seed_data.py           # Script to populate database with sample data
│   └── test_db.py             # Database testing utilities
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── docker-compose.yml         # Docker setup for development
├── Dockerfile                 # Container configuration
└── README.md                  # This file
```

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd birth_certificate_api
```

### 2. Set Up Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
# For development, you can use SQLite (default)
# For production, set DATABASE_URL to PostgreSQL connection string
```

### 3. Install Dependencies

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Run the Application

```bash
# Development server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or run directly
cd app
python main.py
```

The API will be available at: http://localhost:8000

Interactive API documentation: http://localhost:8000/docs

## Docker Setup

### Using Docker Compose (Recommended)

```bash
# Start the application with PostgreSQL
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Using Docker Only

```bash
# Build the image
docker build -t birth-certificate-api .

# Run with SQLite (development)
docker run -p 8000:8000 birth-certificate-api

# Run with external PostgreSQL
docker run -p 8000:8000 -e DATABASE_URL="postgresql://user:pass@host:5432/db" birth-certificate-api
```

## Database Setup

### SQLite (Development)

SQLite is used by default for development. No additional setup required.

### PostgreSQL (Production)

1. Install PostgreSQL server
2. Create database:
   ```sql
   CREATE DATABASE birth_certificate_db;
   CREATE USER birth_cert_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE birth_certificate_db TO birth_cert_user;
   ```
3. Update `.env` file:
   ```bash
   DATABASE_URL=postgresql://birth_cert_user:your_password@localhost:5432/birth_certificate_db
   ```

## API Endpoints

### Birth Certificates

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/birth-certificate/` | Create a new birth certificate |
| GET | `/birth-certificate/{registration_number}` | Get birth certificate by registration number |
| GET | `/birth-certificates/` | List birth certificates (paginated) |

### Request/Response Examples

#### Create Birth Certificate

```bash
curl -X POST "http://localhost:8000/birth-certificate/" \
  -H "Content-Type: application/json" \
  -d '{
    "certificate_info": {
      "title": "Birth Certificate",
      "registration_number": "BC12345678",
      "date_of_issue": "2024-01-15",
      "issuing_authority": "Municipal Corporation",
      "registrar_name": "John Doe"
    },
    "child_info": {
      "name": "Jane Smith",
      "date_of_birth": "2024-01-01",
      "place_of_birth": "New York",
      "sex": "Female"
    },
    "father_info": {
      "name": "John Smith",
      "nationality": "American",
      "profession": "Engineer",
      "residence": "123 Main St, New York",
      "date_of_birth": "1990-05-15",
      "place_of_birth": "Boston"
    },
    "mother_info": {
      "name": "Mary Smith",
      "nationality": "American",
      "profession": "Teacher",
      "residence": "123 Main St, New York",
      "date_of_birth": "1992-08-20",
      "place_of_birth": "Chicago"
    }
  }'
```

#### Get Birth Certificate

```bash
curl "http://localhost:8000/birth-certificate/BC12345678"
```

#### List Birth Certificates

```bash
curl "http://localhost:8000/birth-certificates/?page=1&limit=10"
```

## Data Models

### Birth Certificate Structure

- **Certificate Information**: Title, registration number, issue date, authority, registrar
- **Child Information**: Name, date of birth, place of birth, sex
- **Parent Information**: Name, nationality, profession, residence, date of birth, place of birth

## Development

### Add Sample Data

```bash
# Populate database with sample data
python app/seed_data.py
```

### Test Database Connection

```bash
python app/test_db.py
```

### Running Tests

```bash
# Install test dependencies (included in requirements.txt)
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./birth_certificates.db` |
| `API_HOST` | API server host | `0.0.0.0` |
| `API_PORT` | API server port | `8000` |
| `API_TITLE` | API title | `Birth Certificate Registration API` |
| `ENVIRONMENT` | Environment (development/production) | `development` |
| `DEBUG` | Enable debug mode | `True` |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions, please use the GitHub issue tracker.