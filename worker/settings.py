import configparser

# Load in secrets
config = configparser.ConfigParser()
config.read('keys.ini')

# API keys
GIANTBOMB = config['keys']['giantbomb']
GOODREADS = config['keys']['goodreads']
GOODREADS_ID = config['keys']['goodreads_id']
LASTFM = config['keys']['lastfm']
STEAM = config['keys']['steam']
TMDB = config['keys']['tmdb']
TRAKT = config['keys']['trakt']
TVDB = config['keys']['tvdb']

# User agent
USER_AGENT = 'https://thingsima.de <marcus@thingsima.de>'
