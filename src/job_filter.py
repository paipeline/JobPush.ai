import pandas as pd
from datetime import datetime, timedelta
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class JobFilter:
    def __init__(self, recent_days=4):
        self.recent_days = recent_days

    def load_recent_jobs(self):
        jobs_dir = 'jobs'
        csv_files = [f for f in os.listdir(jobs_dir) if f.endswith('.csv')]
        csv_files.sort(reverse=True)  # 最新的文件排在前面

        all_jobs = []
        cutoff_date = datetime.now().date() - timedelta(days=self.recent_days)

        for file in csv_files:
            file_date = datetime.strptime(file.split('_')[1].split('.')[0], '%Y-%m-%d').date()
            if file_date >= cutoff_date:
                file_path = os.path.join(jobs_dir, file)
                df = pd.read_csv(file_path)
                all_jobs.append(df)
            else:
                break  # 不需要继续检查更早的文件

        if all_jobs:
            return pd.concat(all_jobs, ignore_index=True)
        else:
            return pd.DataFrame()

    def filter_jobs(self, category=None):
        df = self.load_recent_jobs()
        
        if df.empty:
            logger.info("No jobs found in the recent CSV files.")
            return df

        # 确保 'date_posted' 列是日期类型
        df['date_posted'] = pd.to_datetime(df['date_posted']).dt.date

        # 过滤最近几天的工作
        cutoff_date = datetime.now().date() - timedelta(days=self.recent_days)
        df = df[df['date_posted'] >= cutoff_date]

        if category:
            df = df[df['category'] == category]

        df = df.sort_values('date_posted', ascending=False)

        logger.info(f"Filtering jobs for category: {category}")
        logger.info(f"Cutoff date: {cutoff_date}")
        logger.info(f"Total jobs found: {len(df)}")

        if not df.empty:
            logger.info(f"Sample job: {df.iloc[0].to_dict()}")
        else:
            logger.info("No jobs found after filtering.")

        return df
