from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Enum as SQLAlchemyEnum, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from enum import Enum
from typing import List, Optional

Base = declarative_base()

class JobType(Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    CONTRACT = "CONTRACT"
    INTERN = "INTERN"
    TEMPORARY = "TEMPORARY"
    UNKNOWN = "UNKNOWN"

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    company = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    location = Column(String(length=100))
    posted_date = Column(DateTime)
    link = Column(String(500))
    description = Column(Text)
    category = Column(String(100))  # New column added
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    job_type = Column(SQLAlchemyEnum(JobType))

    __table_args__ = (
        UniqueConstraint('title', 'company', 'location', 'job_type', name='uq_job_attributes'),
    )

    def __repr__(self):
        return f"<Job(company='{self.company}', title='{self.title}', location='{self.location}', category='{self.category}')>"
