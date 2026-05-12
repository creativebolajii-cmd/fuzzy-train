import requests

class TelegramAPI:
    def __init__(self, token, channel_id, admin_chat_id=None):
        self.token = token
        self.channel_id = channel_id
        self.admin_chat_id = admin_chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"

    def send_message(self, text, chat_id=None):
        target = chat_id or self.channel_id
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": target,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }
        try:
            response = requests.post(url, json=payload)
            return response.json()
        except Exception as e:
            print(f"Error sending Telegram message: {e}")
            return None

    def send_photo(self, photo_url, caption, chat_id=None):
        target = chat_id or self.channel_id
        url = f"{self.base_url}/sendPhoto"
        payload = {
            "chat_id": target,
            "photo": photo_url,
            "caption": caption,
            "parse_mode": "HTML"
        }
        try:
            response = requests.post(url, json=payload)
            return response.json()
        except Exception as e:
            print(f"Error sending Telegram photo: {e}")
            return None

    def notify_admin(self, message):
        if self.admin_chat_id:
            self.send_message(f"⚠️ <b>Admin Notification:</b>\n{message}", chat_id=self.admin_chat_id)
