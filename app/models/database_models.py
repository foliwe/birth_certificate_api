from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

try:
    # Try relative import first (when used as module)
    from ..database import Base
except ImportError:
    # Fall back to direct import (when running scripts directly)
    from database import Base

class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    registration_number = Column(String, unique=True, index=True)
    date_of_issue = Column(Date)
    issuing_authority = Column(String)
    registrar_name = Column(String)
    
    child = relationship("Child", back_populates="certificate", uselist=False)
    father = relationship(
        "Parent",
        primaryjoin="Certificate.id==Parent.father_of_id",
        back_populates="father_certificates",
        uselist=False
    )
    mother = relationship(
        "Parent",
        primaryjoin="Certificate.id==Parent.mother_of_id",
        back_populates="mother_certificates",
        uselist=False
    )

class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date_of_birth = Column(Date)
    place_of_birth = Column(String)
    sex = Column(String)
    
    certificate_id = Column(Integer, ForeignKey("certificates.id"))
    certificate = relationship("Certificate", back_populates="child")

class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    nationality = Column(String)
    profession = Column(String)
    residence = Column(String)
    date_of_birth = Column(Date)
    place_of_birth = Column(String)

    father_of_id = Column(Integer, ForeignKey("certificates.id"), nullable=True)
    mother_of_id = Column(Integer, ForeignKey("certificates.id"), nullable=True)
    
    father_certificates = relationship("Certificate", foreign_keys=[father_of_id], back_populates="father")
    mother_certificates = relationship("Certificate", foreign_keys=[mother_of_id], back_populates="mother")