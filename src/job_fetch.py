from jobspy import scrape_jobs
import pandas as pd
from datetime import datetime
from utils import is_recent
from database import JobDatabase
from model import JobType
from utils import extract_job_type


def run_job_search(category, search_terms, location):
    all_jobs = pd.DataFrame()
    db = JobDatabase()
    
    for term in search_terms:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        jobs = scrape_jobs(
            site_name=["indeed", "linkedin", "glassdoor"],
            search_term=term,
            location=location,
            results_wanted=2,
            hours_old=72,
            country_indeed='USA',
            headers=headers
        )
        all_jobs = pd.concat([all_jobs, jobs], ignore_index=True)
    
    print(f"找到 {len(all_jobs)} 个 {category} 的工作")
    
    if all_jobs.empty:
        print("----------警告-----------")
        print(f"没有找到 {category} 的工作。跳过进一步处理。")
        return

    # 删除重复项
    all_jobs.drop_duplicates(subset=['job_url'], inplace=True)
    
    # 检查 'date_posted' 列是否存在
    if 'date_posted' not in all_jobs.columns:
        print(f"警告：{category} 没有找到 'date_posted' 列。跳过过滤。")
        filtered_jobs = all_jobs
    else:
        # 过滤最近的工作
        filtered_jobs = all_jobs[all_jobs['date_posted'].apply(is_recent)]

    # 将工作保存到数据库
    for _, job in filtered_jobs.iterrows():
        job_type = extract_job_type(job.get('title', ''))
        job_data = {
            "company": job.get('company', 'N/A'),
            "title": job.get('title', 'N/A'),
            "location": job.get('location', 'N/A'),
            "posted_date": job.get('date_posted', datetime.now()),
            "job_type": JobType[job_type],  # 使用更新后的 job_type
            "link": job.get('job_url', 'N/A'),
            "category": category,
            "description": job.get('description', 'N/A')
        }
        db.create_job(job_data)

    print(f"已将 {len(filtered_jobs)} 个 {category} 的工作保存到数据库")

def main():
    # 定义搜索类别和相应的精确搜索词
    categories = {
        "软件工程": [
            '"Software Engineer Intern"',
            '"Software Developer Intern"',
            '"Programmer Intern"',
            '"Web Developer Intern"',
            '"Mobile App Developer Intern"'
        ],
        "数据科学": [
            '"Data Scientist Intern"',
            '"Data Analyst Intern"',
            '"Machine Learning Intern"',
            '"Big Data Intern"'
        ],
        "人工智能": [
            '"AI Intern"',
            '"Artificial Intelligence Intern"',
            '"Deep Learning Intern"',
            '"NLP Intern"',
            '"Computer Vision Intern"'
        ],
        "音频工程": [
            '"Audio Engineer Intern"',
            '"Sound Engineer Intern"',
        ],
        "游戏开发": [
            '"Game Developer Intern"',
            '"Game Programmer Intern"',
            '"Game Designer Intern"',
            '"Game Animator Intern"'
        ],
        "商业分析": [
            '"Business Analyst Intern"',
            '"Market Research Intern"',
            '"Financial Analyst Intern"',
            '"Operations Research Intern"'
        ],
    }

    # 设置位置
    location = "USA"

    # 对每个类别执行搜索
    for category, search_terms in categories.items():
        run_job_search(category, search_terms, location)

if __name__ == "__main__":
    main()