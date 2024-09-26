from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
DATABASE_URL = 'sqlite:///jobpush.db'
Base = declarative_base(bind=create_async_engine(DATABASE_URL))


class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, unique=True)
    company = Column(String, nullable=True)
    title = Column(String, nullable=True)
    location = Column(String, nullable=True)
    posted_date = Column(DateTime, nullable=True)
    job_type = Column(Enum('FULL_TIME', 'PART_TIME', 'CONTRACT', 'INTERN', name='job_type_enum'), nullable=True)
    link = Column(String, nullable=True)
    description = Column(String, nullable=True)