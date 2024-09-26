from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Enum as SQLAlchemyEnum, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date
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
    posted_date = Column(Date)
    link = Column(String(500))
    description = Column(Text)
    category = Column(String(100))  # 新增列
    created_at = Column(Date, default=date.today)
    updated_at = Column(Date, default=date.today, onupdate=date.today)
    job_type = Column(SQLAlchemyEnum(JobType))

    def __repr__(self):
        return f"<Job(company='{self.company}', title='{self.title}', location='{self.location}', category='{self.category}')>"
