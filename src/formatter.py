# 这个文件将从数据库中获取10个最新的工作机会，并将它们格式化为字符串写入.txt文件
# 清理30天前的数据
from database import JobDatabase
from utils import format_job_info
import os
from pathlib import Path
from datetime import datetime, timedelta

def format_jobs(jobs, category,time_range):
    formatted_jobs = f"📢 今天的{category}工作机会来啦! 快去Apply👉  \n 时间: {datetime.now().strftime('%Y-%m-%d')} \n----------------------------\n\n"
    for job in jobs:
        formatted_jobs += format_job_info(job,time_range)
    return formatted_jobs


def clean_formatted_files(directory: str):
    files = list(Path(directory).glob('formatted_jobs_*_*.txt'))
    thirty_days_ago = datetime.now() - timedelta(days=30)
    if len (files) < 30:
        print("没有超过30天的文件，无需清理")
        return
    for file in files:
        file_date_str = file.stem.split('_')[-1]
        file_date = datetime.strptime(file_date_str, '%Y-%m-%d')
        if file_date < thirty_days_ago:
            try:
                os.remove(file)
                print(f"已删除文件: {file}")
            except Exception as e:
                print(f"无法删除文件 {file}: {e}")
    return

def main():
    db = JobDatabase()
    categories = ["软件工程", "数据科学", "人工智能", "商业分析"]
    for category in categories:
        time_range = 2
        jobs = db.get_recent_jobs_by_category(time_range, category)
        if jobs:
            formatted_content = format_jobs(jobs, category,time_range)
            file_name = f"src/jobs/formatted_jobs_{category}_{datetime.now().strftime('%Y-%m-%d')}.txt"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(formatted_content)
            print(f"已生成{category}的工作机会文件：{file_name}")
        else:
            print(f"没有找到{category}的最新工作机会")
    

if __name__ == "__main__":
    main()