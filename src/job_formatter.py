from datetime import datetime
import pandas as pd

class JobFormatter:
    @staticmethod
    def format_job_info(job):
        title = job['title'].split('(')[0].strip() if pd.notna(job['title']) else "N/A"
        company = job['company'] if pd.notna(job['company']) else "N/A"
        location = job['location'] if pd.notna(job['location']) else "N/A"
        job_type = job['job_type'] if pd.notna(job['job_type']) else "N/A"
        date_posted = job['date_posted'].strftime('%Y-%m-%d') if pd.notna(job['date_posted']) else "N/A"
        job_url = job['job_url'] if pd.notna(job['job_url']) else "N/A"
        category = job['category'] if pd.notna(job['category']) else "N/A"

        return f"""🏢 公司: {company}
💼 职位: {title}
📍 地点: {location}
📅 发布日期: {date_posted}{' 🔥' if (datetime.now().date() - job['date_posted'].date()).days < 2 else ''}
🧢 类型: {job_type}
🔗 链接: {job_url}
🏷️ 类别: {category}
----------------------------
"""

    @classmethod
    def format_all_jobs(cls, jobs_df):
        formatted_jobs = f"📢新的工作机会来啦! 📢今天日期: {datetime.now().strftime('%Y-%m-%d')}\n----------------------------\n\n"
        for _, job in jobs_df.iterrows():
            formatted_jobs += cls.format_job_info(job) + "\n"
        return formatted_jobs
