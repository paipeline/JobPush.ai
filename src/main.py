import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.job_scraper import JobScraper
from src.job_filter import JobFilter
from src.job_formatter import JobFormatter
from src.job_categories import JOB_CATEGORIES
import json
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def save_to_file(content, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    logger.info(f"Saved formatted jobs to {file_path}")

def main():
    try:
        # 读取搜索词配置
        with open('configs/search_terms.json', 'r') as f:
            search_terms = json.load(f)

        # 初始化 JobScraper
        scraper = JobScraper()

        all_jobs = []

        # 对每个类别进行搜索
        for category in search_terms.keys():
            logger.info(f"Scraping jobs for category: {category}")
            jobs = scraper.scrape_jobs(category)
            all_jobs.append(jobs)

        # 合并所有类别的工作
        all_jobs_df = pd.concat(all_jobs, ignore_index=True)

        # 保存到 CSV 文件
        scraper.save_jobs_to_csv(all_jobs_df)

        # 初始化 JobFilter
        job_filter = JobFilter()

        # 过滤和显示每个类别的工作
        for category in JOB_CATEGORIES:
            filtered_jobs = job_filter.filter_jobs(category)
            logger.info(f"Filtered {len(filtered_jobs)} jobs for {category}")

            # 格式化并保存每个类别的工作
            if not filtered_jobs.empty:
                formatted_jobs = JobFormatter.format_all_jobs(filtered_jobs)
                output_file_path = os.path.join('jobs', f'formatted_{category}_jobs.txt')
                save_to_file(formatted_jobs, output_file_path)

        # 获取所有类别的过滤后的工作
        all_filtered_jobs = job_filter.filter_jobs()
        logger.info(f"Total filtered jobs across all categories: {len(all_filtered_jobs)}")

        # 格式化并保存所有过滤后的工作
        if not all_filtered_jobs.empty:
            all_formatted_jobs = JobFormatter.format_all_jobs(all_filtered_jobs)
            all_output_file_path = os.path.join('jobs', 'formatted_all_jobs.txt')
            save_to_file(all_formatted_jobs, all_output_file_path)

    except Exception as e:
        logger.exception(f"An error occurred in main: {str(e)}")

if __name__ == "__main__":
    main()