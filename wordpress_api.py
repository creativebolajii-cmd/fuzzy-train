import requests
from requests.auth import HTTPBasicAuth
import os

class WordPressAPI:
    def __init__(self, url, username, password):
        self.url = url.rstrip('/')
        self.auth = HTTPBasicAuth(username, password)

    def upload_media(self, image_url, title):
        try:
            # Download image first
            img_data = requests.get(image_url).content
            filename = f"{title.replace(' ', '_')}.jpg"
            
            headers = {
                'Content-Disposition': f'attachment; filename={filename}',
                'Content-Type': 'image/jpeg'
            }
            
            response = requests.post(
                f"{self.url}/wp-json/wp/v2/media",
                auth=self.auth,
                headers=headers,
                data=img_data
            )
            if response.status_code == 201:
                return response.json()['id']
            return None
        except Exception as e:
            print(f"Error uploading media: {e}")
            return None

    def create_post(self, movie_data):
        try:
            # 1. Upload featured image
            featured_media_id = self.upload_media(movie_data['poster_url'], movie_data['title'])
            
            # 2. Prepare content
            content = f"""
            <p>{movie_data['description']}</p>
            <hr>
            <p><strong>Download Link:</strong> <a href="{movie_data['download_link']}">{movie_data['title']}</a></p>
            """
            
            # 3. Determine Category ID (Placeholder IDs, user should adjust)
            # In a real setup, we'd fetch categories first
            category_id = 1 # Default
            
            post_data = {
                'title': movie_data['title'],
                'content': content,
                'status': 'publish',
                'categories': [category_id],
                'featured_media': featured_media_id if featured_media_id else 0
            }
            
            response = requests.post(
                f"{self.url}/wp-json/wp/v2/posts",
                auth=self.auth,
                json=post_data
            )
            
            if response.status_code == 201:
                return response.json()['link']
            else:
                print(f"Failed to create post: {response.text}")
                return None
        except Exception as e:
            print(f"Error creating WordPress post: {e}")
            return None
