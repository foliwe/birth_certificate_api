import os
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv

from .database import engine, get_db
from .models import models, database_models
from .models.database_models import Base

# Load environment variables
load_dotenv()

class PaginatedBirthCertificates(BaseModel):
    total: int
    page: int
    limit: int
    data: List[models.BirthCertificate]

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Get configuration from environment variables
API_TITLE = os.getenv("API_TITLE", "Birth Certificate Registration API")
API_VERSION = os.getenv("API_VERSION", "1.0.0")

app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description="A comprehensive API for managing birth certificate registrations",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint with API information."""
    return {
        "message": "Birth Certificate Registration API",
        "version": API_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "api": API_TITLE, "version": API_VERSION}

@app.post("/birth-certificate/", response_model=models.BirthCertificate)
def create_birth_certificate(birth_certificate: models.BirthCertificate, db: Session = Depends(get_db)):
    # Create certificate
    db_certificate = database_models.Certificate(
        title=birth_certificate.certificate_info.title,
        registration_number=birth_certificate.certificate_info.registration_number,
        date_of_issue=birth_certificate.certificate_info.date_of_issue,
        issuing_authority=birth_certificate.certificate_info.issuing_authority,
        registrar_name=birth_certificate.certificate_info.registrar_name
    )
    db.add(db_certificate)
    db.flush()

    # Create child
    db_child = database_models.Child(
        name=birth_certificate.child_info.name,
        date_of_birth=birth_certificate.child_info.date_of_birth,
        place_of_birth=birth_certificate.child_info.place_of_birth,
        sex=birth_certificate.child_info.sex,
        certificate_id=db_certificate.id
    )
    db.add(db_child)

    # Create father
    db_father = database_models.Parent(
        name=birth_certificate.father_info.name,
        nationality=birth_certificate.father_info.nationality,
        profession=birth_certificate.father_info.profession,
        residence=birth_certificate.father_info.residence,
        date_of_birth=birth_certificate.father_info.date_of_birth,
        place_of_birth=birth_certificate.father_info.place_of_birth,
        father_of_id=db_certificate.id
    )
    db.add(db_father)

    # Create mother
    db_mother = database_models.Parent(
        name=birth_certificate.mother_info.name,
        nationality=birth_certificate.mother_info.nationality,
        profession=birth_certificate.mother_info.profession,
        residence=birth_certificate.mother_info.residence,
        date_of_birth=birth_certificate.mother_info.date_of_birth,
        place_of_birth=birth_certificate.mother_info.place_of_birth,
        mother_of_id=db_certificate.id
    )
    db.add(db_mother)

    db.commit()
    db.refresh(db_certificate)
    
    return birth_certificate

@app.get("/birth-certificate/{registration_number}", response_model=models.BirthCertificate)
def get_birth_certificate(registration_number: str, db: Session = Depends(get_db)):
    certificate = db.query(database_models.Certificate).filter(
        database_models.Certificate.registration_number == registration_number
    ).first()
    
    if certificate is None:
        raise HTTPException(status_code=404, detail="Birth certificate not found")
    
    return models.BirthCertificate(
        certificate_info=models.CertificateInformation(
            title=certificate.title,
            registration_number=certificate.registration_number,
            date_of_issue=certificate.date_of_issue,
            issuing_authority=certificate.issuing_authority,
            registrar_name=certificate.registrar_name
        ),
        child_info=models.ChildInformation(
            name=certificate.child.name,
            date_of_birth=certificate.child.date_of_birth,
            place_of_birth=certificate.child.place_of_birth,
            sex=certificate.child.sex
        ),
        father_info=models.ParentInformation(
            name=certificate.father.name,
            nationality=certificate.father.nationality,
            profession=certificate.father.profession,
            residence=certificate.father.residence,
            date_of_birth=certificate.father.date_of_birth,
            place_of_birth=certificate.father.place_of_birth
        ),
        mother_info=models.ParentInformation(
            name=certificate.mother.name,
            nationality=certificate.mother.nationality,
            profession=certificate.mother.profession,
            residence=certificate.mother.residence,
            date_of_birth=certificate.mother.date_of_birth,
            place_of_birth=certificate.mother.place_of_birth
        )
    )

@app.get("/birth-certificates/", response_model=PaginatedBirthCertificates)
def get_birth_certificates(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    try:
        # Calculate skip (offset) based on page and limit
        skip = (page - 1) * limit
        
        # Get total count of records
        total = db.query(database_models.Certificate).count()
        print(f"Total records in database: {total}")

        # Get certificates with all related data in a single query
        certificates = (
            db.query(database_models.Certificate)
            .options(
                joinedload(database_models.Certificate.child),
                joinedload(database_models.Certificate.father),
                joinedload(database_models.Certificate.mother)
            )
            .order_by(database_models.Certificate.registration_number)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
        # Print debug information
        print(f"Retrieved {len(certificates)} certificates")
        for cert in certificates:
            print(f"Certificate {cert.registration_number}:")
            print(f"  Child: {cert.child.name if cert.child else 'None'}")
            print(f"  Father: {cert.father.name if cert.father else 'None'}")
            print(f"  Mother: {cert.mother.name if cert.mother else 'None'}")
        
        # Convert to response model
        birth_certificates = []
        for cert in certificates:
            try:
                print(f"Processing certificate: {cert.registration_number}")
                certificate_data = models.BirthCertificate(
                    certificate_info=models.CertificateInformation(
                        title=cert.title,
                        registration_number=cert.registration_number,
                        date_of_issue=cert.date_of_issue,
                        issuing_authority=cert.issuing_authority,
                        registrar_name=cert.registrar_name
                    ),
                    child_info=models.ChildInformation(
                        name=cert.child.name if cert.child else "Unknown",
                        date_of_birth=cert.child.date_of_birth if cert.child else None,
                        place_of_birth=cert.child.place_of_birth if cert.child else "Unknown",
                        sex=cert.child.sex if cert.child else "Unknown"
                    ) if cert.child else None,
                    father_info=models.ParentInformation(
                        name=cert.father.name if cert.father else "Unknown",
                        nationality=cert.father.nationality if cert.father else "Unknown",
                        profession=cert.father.profession if cert.father else "Unknown",
                        residence=cert.father.residence if cert.father else "Unknown",
                        date_of_birth=cert.father.date_of_birth if cert.father else None,
                        place_of_birth=cert.father.place_of_birth if cert.father else "Unknown"
                    ) if cert.father else None,
                    mother_info=models.ParentInformation(
                        name=cert.mother.name if cert.mother else "Unknown",
                        nationality=cert.mother.nationality if cert.mother else "Unknown",
                        profession=cert.mother.profession if cert.mother else "Unknown",
                        residence=cert.mother.residence if cert.mother else "Unknown",
                        date_of_birth=cert.mother.date_of_birth if cert.mother else None,
                        place_of_birth=cert.mother.place_of_birth if cert.mother else "Unknown"
                    ) if cert.mother else None
                )
                birth_certificates.append(certificate_data)
                print(f"Successfully processed certificate: {cert.registration_number}")
            except Exception as e:
                print(f"Error processing certificate {cert.registration_number}: {str(e)}")
                continue
        
        return PaginatedBirthCertificates(
            total=total,
            page=page,
            limit=limit,
            data=birth_certificates
        )
    except Exception as e:
        print(f"Error in get_birth_certificates: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment variables
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        app, 
        host=host, 
        port=port, 
        reload=debug,
        log_level="info" if not debug else "debug"
    )