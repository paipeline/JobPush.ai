from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from model import Job, Base  # 确保从你的模型文件中导入 Job 和 Base
from database import SessionLocal  # 假设你有一个数据库连接的模块
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from models import Job

def normalize_existing_job_types(session: Session):
    jobs = session.query(Job).all()
    for job in jobs:
        if job.job_type == 'parttime':
            job.job_type = 'PART_TIME'
        elif job.job_type not in ('FULL_TIME', 'PART_TIME', 'CONTRACT', 'INTERN', 'PARTTIME', 'TEMPORARY'):
            job.job_type = 'UNKNOWN'
    session.commit()

# 在创建数据库会话后立即调用这个函数
engine = create_engine('your_database_url')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
normalize_existing_job_types(db)
db.close()

app = FastAPI()


@app.get('/jobs/all')
async def get_jobs_all():
    # 获取过去两天的工作
    two_days_ago = datetime.now() - timedelta(days=2)
    db: Session = SessionLocal()  # 创建数据库会话
    try:
        jobs = db.query(Job).filter(Job.posted_date >= two_days_ago).all()  # 查询过去两天的工作
        return JSONResponse(content=[job.__dict__ for job in jobs])  # 返回工作数据
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get('/jobs/companies')
async def get_jobs_companies():
    db: Session = SessionLocal() 
    try:
        companies_jobs = db.query(Job.company, Job.title).distinct().all()  # 查询所有公司的工作
        return JSONResponse(content=[{"company": job[0], "title": job[1]} for job in companies_jobs])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get('/jobs/by_company/{company_name}')
async def get_jobs_by_company(company_name: str):
    db: Session = SessionLocal()
    try:
        jobs = db.query(Job).filter(Job.company == company_name).all()
        return JSONResponse(content=[job.__dict__ for job in jobs])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
