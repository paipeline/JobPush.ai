import csv
from jobspy import scrape_jobs
import pandas as pd
from datetime import datetime, timedelta
import re
import os

def extract_location(title):
    match = re.search(r'\((.*?)\)', title)
    return match.group(1) if match else "N/A"

def extract_job_type(title):
    types = ["INTERN", "CO-OP", "FULL-TIME", "PART-TIME"]
    for job_type in types:
        if job_type.lower() in title.lower():
            return job_type
    return "N/A"

def format_job_info(row):
    title = row['title'].split('(')[0].strip()
    location = row['location'] if pd.notna(row['location']) else "N/A"
    job_type = row['job_type'] if pd.notna(row['job_type']) else extract_job_type(row['title'])
    date_posted = row['date_posted'] if pd.notna(row['date_posted']) else "N/A"
    job_url = row['job_url'] if pd.notna(row['job_url']) else "N/A"

    return f"""🏢 公司: {row['company']}
💼 职位: {title}
📍 地点: {location}
📅 发布日期: {date_posted}{' 🔥' if (datetime.now().date() - datetime.strptime(str(date_posted), '%Y-%m-%d').date()).days < 2 else ''}
🧢 类型: {job_type}
🔗 链接: {job_url}
----------------------------
"""

def is_recent(date_posted):
    if pd.isna(date_posted):
        return False
    today = datetime.now().date()
    two_days_ago = today - timedelta(days=4)
    return str(date_posted) >= str(two_days_ago)

def is_relevant(title):
    keywords = ['software developer', 'data science', 'intern', 'co-op']
    return any(keyword in title.lower() for keyword in keywords)

# 确保 jobs 文件夹存在
if not os.path.exists('jobs'):
    os.makedirs('jobs')

# 抓取工作信息
jobs = scrape_jobs(
    site_name=["indeed", "linkedin", "glassdoor"],
    search_term="software engineer intern",
    results_wanted=50,
    hours_old=42,
    country_indeed='USA',
)

print(f"Found {len(jobs)} jobs")

jobs_file_path = os.path.join('jobs', 'jobs.csv')
jobs.to_csv(jobs_file_path, index=False)
print(f"Saved scraped jobs to {jobs_file_path}")
jobs = pd.read_csv(jobs_file_path)

print(f"Found {len(jobs)} jobs")

# 过滤和格式化工作信息
filtered_jobs = jobs[['title', 'company', 'location', 'job_type', 'date_posted', 'description', 'job_url']].copy()

# 只保留最近两天发布的相关工作
filtered_jobs = filtered_jobs[
    filtered_jobs['date_posted'].apply(is_recent) & 
    filtered_jobs['title'].apply(is_relevant)
]

# 格式化输出
formatted_jobs = f"📢新的工作机会来啦! 📢今天日期: {datetime.now().strftime('%Y-%m-%d')}\n----------------------------\n\n"
formatted_jobs += filtered_jobs.apply(format_job_info, axis=1).str.cat(sep='\n')
print(formatted_jobs)

# 保存过滤后的工作到文本文件
output_file_path = os.path.join('jobs', 'filtered_recent_jobs.txt')
with open(output_file_path, "w", encoding='utf-8') as f:
    f.write(formatted_jobs)

print(f"Filtered recent jobs saved to {output_file_path}")


