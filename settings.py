import configparser

# Load in secrets
config = configparser.ConfigParser()
config.read('keys.ini')

# API keys
GIANTBOMB = config['keys']['giantbomb']
GOODREADS = config['keys']['goodreads']
LASTFM = config['keys']['lastfm']
STEAM = config['keys']['steam']
TMDB = config['keys']['tmdb']
TRAKT = config['keys']['trakt']

# User agent
USER_AGENT = { 'User-Agent': 'https://thingsima.de <marcus@thingsima.de>' }