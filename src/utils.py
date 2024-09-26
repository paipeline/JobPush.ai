import pandas as pd
from datetime import datetime, timedelta
from model import JobType, Job

def extract_job_type(title):
    types = {
        "INTERN": "实习",
        "CO-OP": "合作",
        "FULL-TIME": "全职",
        "PART-TIME": "兼职"
    }
    for job_type, chinese_type in types.items():
        if job_type.lower() in title.lower() or chinese_type in title:
            return job_type
    return "UNKNOWN"  # 返回 "UNKNOWN" 而不是 "N/A"


def format_job_info(job: Job,time_range):
    title = job.title.split('(')[0].strip()
    location = job.location if job.location else "N/A"
    job_type = job.job_type if job.job_type else extract_job_type(job.title)
    date_posted = job.posted_date if job.posted_date else "N/A"
    job_url = job.link if job.link else "N/A"
    print(date_posted)
    print(datetime.now().date())
    return f"""📅 发布日期: {date_posted}{' 🔥' if date_posted == datetime.now().date() else ''}
🏢 公司: {job.company}
💼 岗位: {title}
📍 地点: {location}
👋 类型: {job_type}
🔗 链接: {job_url}
----------------------------
"""


def is_recent(date_posted):
    if pd.isna(date_posted):
        return False
    today = datetime.now().date()
    four_days_ago = today - timedelta(days=4)
    return str(date_posted) >= str(four_days_ago)


