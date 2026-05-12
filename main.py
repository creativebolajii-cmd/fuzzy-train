import time
import schedule
import logging
from scraper import MovieScraper
from wordpress_api import WordPressAPI
from telegram_api import TelegramAPI
from formatter import Formatter
import config
import os

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("automation.log"),
        logging.StreamHandler()
    ]
)

class AwakeMoviesAutomation:
    def __init__(self):
        self.scraper = MovieScraper()
        self.wp = WordPressAPI(
            config.WP_CONFIG['url'],
            config.WP_CONFIG['username'],
            config.WP_CONFIG['password']
        )
        self.tg = TelegramAPI(
            config.TELEGRAM_CONFIG['token'],
            config.TELEGRAM_CONFIG['channel_id'],
            config.TELEGRAM_CONFIG['admin_chat_id']
        )
        self.formatter = Formatter()
        self.posted_log = "posted_log.txt"

    def is_already_posted(self, title):
        if not os.path.exists(self.posted_log):
            return False
        with open(self.posted_log, 'r') as f:
            posted_titles = f.read().splitlines()
        return title in posted_titles

    def log_posted(self, title):
        with open(self.posted_log, 'a') as f:
            f.write(f"{title}\n")

    def run_job(self):
        logging.info("Starting automation job...")
        try:
            movies = self.scraper.scrape_all()
            count = 0
            
            for movie in movies:
                if count >= config.POSTS_PER_RUN:
                    break
                
                if self.is_already_posted(movie['title']):
                    logging.info(f"Skipping already posted: {movie['title']}")
                    continue
                
                logging.info(f"Processing: {movie['title']}")
                
                # 1. Post to WordPress
                wp_url = self.wp.create_post(movie)
                if not wp_url:
                    logging.error(f"Failed to post to WordPress: {movie['title']}")
                    self.tg.notify_admin(f"Failed to post to WordPress: {movie['title']}")
                    continue
                
                logging.info(f"Posted to Website: {wp_url}")
                
                # 2. Post to Telegram
                if movie['type'] == "Series":
                    caption = self.formatter.format_series(movie, wp_url)
                else:
                    caption = self.formatter.format_movie(movie, wp_url)
                
                tg_res = self.tg.send_photo(movie['poster_url'], caption)
                if tg_res and tg_res.get('ok'):
                    logging.info(f"Posted to Telegram: {movie['title']}")
                else:
                    logging.error(f"Failed to post to Telegram: {movie['title']}")
                    self.tg.notify_admin(f"Failed to post to Telegram: {movie['title']}")
                
                # 3. Log and Delay
                self.log_posted(movie['title'])
                count += 1
                
                if count < config.POSTS_PER_RUN:
                    logging.info(f"Waiting {config.DELAY_BETWEEN_POSTS} seconds before next post...")
                    time.sleep(config.DELAY_BETWEEN_POSTS)
            
            logging.info(f"Job finished. Posted {count} items.")
            
        except Exception as e:
            logging.error(f"Error in automation job: {e}")
            self.tg.notify_admin(f"Automation job failed: {e}")

def start_scheduler():
    automation = AwakeMoviesAutomation()
    # Run once immediately
    automation.run_job()
    
    # Schedule every 2 hours
    schedule.every(config.SCHEDULE_INTERVAL_HOURS).hours.do(automation.run_job)
    
    logging.info(f"Scheduler started. Running every {config.SCHEDULE_INTERVAL_HOURS} hours.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler()
