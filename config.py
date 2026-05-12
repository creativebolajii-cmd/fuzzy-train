import os
from dotenv import load_dotenv

load_dotenv()

# Scraper Settings
SOURCE_SITES = [
    "https://9jarocks.net",
    "https://thenkiri.com",
    "https://naijaprey.tv",
    "https://mysmartmedia.com.ng",
    "https://seriezloaded.com.ng",
    "https://movies.sureloaded.net"
]

# Automation Settings
POSTS_PER_RUN = 3
DELAY_BETWEEN_POSTS = 300  # 5 minutes in seconds
SCHEDULE_INTERVAL_HOURS = 2

# Database Settings
DB_PATH = "sqlite:///awakemovies.db"

# Branding Colors
COLORS = {
    "background": "#def1ff",
    "primary": "#0374a8"
}

# WordPress Config
WP_CONFIG = {
    "url": os.getenv("WP_SITE_URL"),
    "username": os.getenv("WP_USERNAME"),
    "password": os.getenv("WP_APP_PASSWORD")
}

# Telegram Config
TELEGRAM_CONFIG = {
    "token": os.getenv("TELEGRAM_BOT_TOKEN"),
    "channel_id": os.getenv("TELEGRAM_CHANNEL_ID"),
    "admin_chat_id": os.getenv("TELEGRAM_ADMIN_CHAT_ID")
}

# Email Config
EMAIL_CONFIG = {
    "sender": os.getenv("EMAIL_SENDER"),
    "password": os.getenv("EMAIL_PASSWORD"),
    "receiver": os.getenv("EMAIL_RECEIVER")
}
