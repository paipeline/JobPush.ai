import logging
from jobspy import scrape_jobs
import pandas as pd
from datetime import datetime
import json
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class JobScraper:
    def __init__(self, site_names=None, country='USA'):
        self.site_names = site_names or ["indeed", "linkedin", "glassdoor"]
        self.country = country
        with open('configs/search_terms.json', 'r') as f:
            self.search_terms = json.load(f)

    def scrape_jobs(self, category, results_wanted=10, hours_old=42):
        jobs = []
        for search_term in self.search_terms[category]:
            try:
                scraped_jobs = scrape_jobs(
                    site_name=self.site_names,
                    search_term=search_term,
                    results_wanted=results_wanted,
                    hours_old=hours_old,
                    country_indeed=self.country,
                    pages=1
                )
                jobs.extend(scraped_jobs)
            except Exception as e:
                logger.error(f"Error scraping jobs for term '{search_term}': {str(e)}")
        
        df = pd.DataFrame(jobs)
        df['category'] = category
        logger.info(f"Scraped {len(df)} jobs for category: {category}")
        logger.info("--------------------------------------------------")
        return df

    def save_jobs_to_csv(self, all_jobs_df):
        today = datetime.now().strftime('%Y-%m-%d')
        file_name = f'jobs_{today}.csv'
        file_path = os.path.join('jobs', file_name)
        
        os.makedirs('jobs', exist_ok=True)
        
        all_jobs_df.to_csv(file_path, index=False, encoding='utf-8')
        
        logger.info(f"Saved {len(all_jobs_df)} jobs to {file_path}")

    def log_dataframe_info(self, df):
        logger.info(f"DataFrame shape: {df.shape}")
        logger.info(f"DataFrame columns: {df.columns.tolist()}")
        logger.info(f"DataFrame info:\n{df.info()}")
        logger.info(f"First few rows:\n{df.head().to_string()}")
