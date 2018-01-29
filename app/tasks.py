import settings
from utils import update_books, update_movies, update_music, update_shows

def update_stats():
    update_books()
    update_movies()
    update_music()
    update_shows()

update_stats()
