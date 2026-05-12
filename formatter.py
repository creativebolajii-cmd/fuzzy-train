class Formatter:
    @staticmethod
    def format_movie(movie_data, post_url):
        template = (
            "🚨 <b>New Upload Alert on AWAKEMOVIES!</b>\n"
            "We've just added a top-rated MOVIE for your entertainment:\n\n"
            "🎬 <b>Download {title} ({year})</b>\n"
            "📅 Year: {year}\n"
            "🌍 Genre: {genre}\n"
            "📺 Language: {language}\n"
            "⭐️ IMDb Rating: {rating}/10\n\n"
            "Movie Summary: {description}\n\n"
            "📥 <a href='{post_url}'>Click here to Download in HD</a>\n\n"
            "Note: Open the link in Chrome or your main browser.\n"
            "Avoid using Telegram's in-app browser.\n\n"
            "Also join our TikTok for recommendations 👇\n"
            "https://www.tiktok.com/@awakemovies.tv"
        )
        return template.format(
            title=movie_data['title'],
            year=movie_data['year'],
            genre=movie_data['genre'],
            language=movie_data['language'],
            rating=movie_data['rating'],
            description=movie_data['description'][:200] + "..." if len(movie_data['description']) > 200 else movie_data['description'],
            post_url=post_url
        )

    @staticmethod
    def format_series(movie_data, post_url):
        template = (
            "🚨 <b>New Upload Alert on AWAKEMOVIES!</b>\n"
            "We've just added a top-rated SERIES for your entertainment:\n\n"
            "🎬 <b>Download {title} S{season} ({episodes})</b>\n"
            "📅 Year: {year}\n"
            "🌍 Genre: {genre}\n"
            "📺 Language: {language}\n"
            "⭐️ IMDb Rating: {rating}/10\n\n"
            "Series Summary: {description}\n\n"
            "📥 <a href='{post_url}'>Click here to Download in HD</a>\n\n"
            "Note: Open the link in Chrome or your main browser.\n"
            "Avoid using Telegram's in-app browser.\n\n"
            "Also join our TikTok for recommendations 👇\n"
            "https://www.tiktok.com/@awakemovies.tv"
        )
        return template.format(
            title=movie_data['title'],
            season=movie_data['season'],
            episodes=movie_data['episodes'],
            year=movie_data['year'],
            genre=movie_data['genre'],
            language=movie_data['language'],
            rating=movie_data['rating'],
            description=movie_data['description'][:200] + "..." if len(movie_data['description']) > 200 else movie_data['description'],
            post_url=post_url
        )
