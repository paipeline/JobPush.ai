from sqlalchemy import create_engine, Column, Integer, String, Date, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import enum
from job_categories import JobCategory
Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255))
    job_type = Column(String(50))
    date_posted = Column(Date)
    description = Column(Text)
    job_url = Column(String(512))
    category = Column(Enum(JobCategory))

    def __repr__(self):
        return f"<Job(title='{self.title}', company='{self.company}', category='{self.category.value}', date_posted='{self.date_posted}')>"

# 数据库连接配置
DATABASE_URL = "postgresql://bloguser:332522@localhost/job_search_db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")