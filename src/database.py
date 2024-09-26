from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Job, Base
from typing import Optional, List
from datetime import datetime
from model import JobType

class JobDatabase:
    def __init__(self, db_url: str = 'sqlite:///jobpush.db'):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_job(self, job_data: dict) -> Optional[Job]:
        session = self.Session()
        try:
            # 检查是否已存在满足约束条件的作业
            existing_job = session.query(Job).filter(
                Job.title == job_data.get('title'),
                Job.company == job_data.get('company'),
            ).first()

            if existing_job:
                print(f"已存在: {existing_job}")
                return existing_job

            new_job = Job(**job_data)
            session.add(new_job)
            session.commit()
            session.refresh(new_job)
            return new_job
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_job_by_id(self, job_id: int) -> Optional[Job]:
        session = self.Session()
        try:
            return session.query(Job).filter(Job.id == job_id).first()
        finally:
            session.close()

    def get_all_jobs(self) -> List[Job]:
        session = self.Session()
        try:
            return session.query(Job).all()
        finally:
            session.close()

    def update_job(self, job_id: int, job_data: dict) -> Optional[Job]:
        session = self.Session()
        try:
            job = session.query(Job).filter(Job.id == job_id).first()
            if job:
                for key, value in job_data.items():
                    setattr(job, key, value)
                session.commit()
                session.refresh(job)  # Refresh the job object
                return job
            return None
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_job(self, job_id: int) -> bool:
        session = self.Session()
        try:
            job = session.query(Job).filter(Job.id == job_id).first()
            if job:
                session.delete(job)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def search_jobs(self, **kwargs) -> List[Job]:
        session = self.Session()
        try:
            query = session.query(Job)
            for key, value in kwargs.items():
                if hasattr(Job, key):
                    query = query.filter(getattr(Job, key).like(f"%{value}%"))
            return query.all()
        finally:
            session.close()

# Example usage
if __name__ == "__main__":
    db = JobDatabase()
    new_job_data = {
        "company": "Norfolk",
        "title": "IT Computer Vision Intern - Spring 2025",
        "location": "Atlanta, GA",
        "posted_date": datetime(2024, 9, 17),
        "job_type": JobType.INTERN,
        "link": "https://www.linkedin.com/jobs/view/4026045302",
        "category": "人工智能"  # New field added
    }
    created_job = db.create_job(new_job_data)

    # # Get all jobs
    # all_jobs = db.get_all_jobs()
    # print(f"All jobs: {all_jobs}")

    # # Update a job
    # updated_job = db.update_job(created_job.id, {"title": "Updated IT Computer Vision Intern"})
    # print(f"Updated job: {updated_job}")


    # # Search for jobs
    # search_results = db.search_jobs(company="Norfolk", category="人工智能")
    # print(f"Search results: {search_results}")

    # # Delete a job
    # deleted = db.delete_job(created_job.id)
    # print(f"Job deleted: {deleted}")
    