import requests
from bs4 import BeautifulSoup
import time
import re

class MovieScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_soup(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'lxml')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def scrape_9jarocks(self):
        url = "https://9jarocks.net"
        soup = self.get_soup(url)
        if not soup:
            return []

        movies = []
        # Logic to find post links on 9jarocks
        # This is a placeholder for the actual selector which depends on the site's structure
        # Typically: soup.find_all('article') or soup.select('.post-item')
        posts = soup.select('article.post-item') or soup.select('.post')
        
        for post in posts[:10]: # Check first 10 posts
            link_tag = post.find('a')
            if not link_tag: continue
            
            post_url = link_tag['href']
            movie_data = self.scrape_9jarocks_detail(post_url)
            if movie_data:
                movies.append(movie_data)
        
        return movies

    def scrape_9jarocks_detail(self, url):
        soup = self.get_soup(url)
        if not soup: return None
        
        try:
            title = soup.find('h1').text.strip() if soup.find('h1') else "Unknown Title"
            
            # Extract Year, Genre, etc. using regex or specific selectors
            content_text = soup.get_text()
            
            year_match = re.search(r'Year:\s*(\d{4})', content_text)
            year = year_match.group(1) if year_match else "N/A"
            
            genre_match = re.search(r'Genre:\s*([^\n]+)', content_text)
            genre = genre_match.group(1).strip() if genre_match else "N/A"
            
            lang_match = re.search(r'Language:\s*([^\n]+)', content_text)
            language = lang_match.group(1).strip() if lang_match else "English"
            
            imdb_match = re.search(r'IMDb Rating:\s*([\d\.]+)', content_text)
            rating = imdb_match.group(1) if imdb_match else "0.0"
            
            # Description
            desc_tag = soup.select_one('.entry-content p')
            description = desc_tag.text.strip() if desc_tag else "No description available."
            
            # Poster
            img_tag = soup.select_one('.entry-content img') or soup.select_one('article img')
            poster_url = img_tag['src'] if img_tag else ""
            
            # Download Link
            download_tag = soup.find('a', href=re.compile(r'download', re.I))
            download_link = download_tag['href'] if download_tag else ""
            
            # Classification
            is_series = any(x in title.upper() for x in ["S01", "SEASON", "EPISODE", "COMPLETE"])
            season = ""
            episodes = ""
            if is_series:
                s_match = re.search(r'S(\d+)', title, re.I) or re.search(r'Season\s*(\d+)', title, re.I)
                season = s_match.group(1) if s_match else "1"
                e_match = re.search(r'E(\d+)-E(\d+)', title, re.I) or re.search(r'Episode\s*(\d+)', title, re.I)
                episodes = e_match.group(0) if e_match else "Full"

            return {
                "title": title,
                "year": year,
                "genre": genre,
                "language": language,
                "rating": rating,
                "description": description,
                "poster_url": poster_url,
                "download_link": download_link,
                "type": "Series" if is_series else "Movie",
                "season": season,
                "episodes": episodes,
                "source_url": url
            }
        except Exception as e:
            print(f"Error parsing detail {url}: {e}")
            return None

    def scrape_all(self):
        all_movies = []
        all_movies.extend(self.scrape_9jarocks())
        # Other sites would follow similar patterns
        return all_movies
