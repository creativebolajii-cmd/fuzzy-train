# AwakeMovies Automation Tool

This project provides a comprehensive Python-based automation tool for the AwakeMovies website. It automates the process of scraping new movie and series posts from various source websites, posting them to a WordPress site, and then sharing them on a Telegram channel. Additionally, it includes a Flask-based web dashboard for monitoring and managing the automation process.

## Features

- **Multi-site Scraping**: Scrapes movie and series data from multiple predefined websites.
- **WordPress Integration**: Automatically creates new posts on your WordPress site with extracted details, including featured images and download links.
- **Duplicate Prevention**: Maintains a log of posted titles to avoid re-posting content.
- **Error Handling & Notifications**: Logs errors and sends Telegram notifications to an admin chat in case of posting failures.
- **Scheduled Automation**: Runs automatically at specified intervals (e.g., every 2 hours).
- **Configurable**: Easy customization of scraping sources, posting frequency, and API credentials via `config.py` and `.env` file.
- **Web Dashboard**: A Flask application for:
    - Overview of posted movies/series.
    - Basic statistics (total posted, posted today).
    - Settings management (simulated).
    - Admin/User authentication.

## Project Structure

```
awakemovies_tool/
├── main.py                 # Main automation script and scheduler
├── scraper.py              # Logic for scraping movie/series data from source websites
├── wordpress_api.py        # Handles interactions with the WordPress REST API
├── telegram_api.py         # Handles interactions with the Telegram Bot API
├── formatter.py            # Formats messages for Telegram posts
├── config.py               # Centralized configuration settings
├── .env.example            # Template for environment variables (API keys, passwords)
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── dashboard.py            # Flask web application for the dashboard
├── templates/
│   ├── index.html          # Dashboard homepage template
│   ├── login.html          # Login page template
│   ├── movies.html         # All movies listing template
│   └── settings.html       # Settings page template
└── static/
    └── ...                 # Static assets (CSS, JS, images - currently empty)
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository_url>
cd awakemovies_tool
```

### 2. Create and Activate a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the `.env.example` file to `.env` and fill in your credentials.

```bash
cp .env.example .env
```

Edit the `.env` file with your actual WordPress, Telegram, and Email API details:

```ini
# WordPress API Credentials
WP_SITE_URL=https://awakemovies.com
WP_USERNAME=your_wordpress_username
WP_APP_PASSWORD=your_wordpress_application_password

# Telegram API Credentials
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL_ID=@your_telegram_channel_username_or_id
TELEGRAM_ADMIN_CHAT_ID=your_personal_telegram_chat_id_for_notifications

# Email Credentials (for notifications)
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_email_app_password # For Gmail, generate an App Password
EMAIL_RECEIVER=receiver_email@gmail.com # Email to receive success notifications

# Dashboard Settings
SECRET_KEY=a_long_random_string_for_flask_session_security
ADMIN_PASSWORD=your_dashboard_admin_password
```

**Note on WordPress Application Passwords**: You can generate an application password in your WordPress dashboard under `Users > Profile > Application Passwords`.

**Note on Telegram Bot Token**: Create a new bot via BotFather on Telegram to get your token.

**Note on Telegram Channel ID**: For a public channel, use `@channelusername`. For a private channel, you might need to use a bot to get the channel ID (e.g., by forwarding a message from the channel to `@get_id_bot`).

**Note on Telegram Admin Chat ID**: This is your personal Telegram chat ID where the bot will send failure notifications. You can get it from `@get_id_bot`.

**Note on Email App Password**: If you are using Gmail, you will need to generate an App Password as direct password usage is often blocked for security reasons. Refer to Google's documentation on how to generate one.

### 5. Initialize the Database (for Dashboard)

Run the dashboard script once to initialize the SQLite database and create the default admin user.

```bash
python dashboard.py
```

This will create `awakemovies.db` and an admin user with username `admin` and the password specified in `ADMIN_PASSWORD` in your `.env` file (defaults to `admin123` if not set).

### 6. Run the Automation Tool

To start the main automation script with the scheduler:

```bash
python main.py
```

The script will run an automation job immediately and then schedule subsequent runs every 2 hours (as defined in `config.py`).

### 7. Run the Web Dashboard

To start the Flask web dashboard:

```bash
python dashboard.py
```

The dashboard will be accessible at `http://127.0.0.1:5000` (or `http://localhost:5000`). Log in with the admin credentials you set up.

## Customization

- **`config.py`**: Adjust scraping sources, posting limits, and delays.
- **`scraper.py`**: Add new scraping logic for additional websites by creating new methods (e.g., `scrape_thenkiri`) and integrating them into `scrape_all`.
- **`formatter.py`**: Modify Telegram message templates.
- **Branding Colors**: Change `#def1ff` (background) and `#0374a8` (primary deep teal) in `config.py` to match your brand.

## Extending the Scraper

To add a new scraping source (e.g., `thenkiri.com`):

1.  **Add URL to `config.py`**: Add the new website URL to the `SOURCE_SITES` list.
2.  **Create a new scraping method in `scraper.py`**: Define a method like `scrape_thenkiri(self)` that fetches content from the new site, extracts movie/series data, and returns it in the standardized dictionary format.
3.  **Integrate into `scrape_all`**: Call your new scraping method from `MovieScraper.scrape_all()`.

Example for `thenkiri.com` (conceptual):

```python
# In scraper.py

    def scrape_thenkiri(self):
        url = "https://thenkiri.com"
        soup = self.get_soup(url)
        if not soup:
            return []

        movies = []
        # Implement scraping logic for thenkiri.com
        # ... find posts, extract details ...
        return movies

    def scrape_all(self):
        all_movies = []
        all_movies.extend(self.scrape_9jarocks())
        all_movies.extend(self.scrape_thenkiri()) # Add this line
        # ... add other sites ...
        return all_movies
```

## Troubleshooting

- **`KeyError` or `AttributeError` in Scraper**: This usually means the website structure has changed, and the CSS selectors or regex patterns in `scraper.py` need to be updated.
- **WordPress Posting Fails**: Check your `WP_USERNAME` and `WP_APP_PASSWORD` in `.env`. Ensure the WordPress REST API is enabled and accessible.
- **Telegram Messages Not Sending**: Verify `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHANNEL_ID`, and `TELEGRAM_ADMIN_CHAT_ID` in `.env`. Ensure the bot has necessary permissions in the channel.
- **Scheduler Not Running**: Ensure `main.py` is running continuously. If running in a temporary environment, it might stop when the environment closes.

## License

This project is open-source and available under the MIT License. See the `LICENSE` file for more details. (Note: A `LICENSE` file is not included in this deliverable but can be added.)
