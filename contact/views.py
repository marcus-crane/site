from django.conf import settings
from django.shortcuts import render
import requests

def contact(request):
  url = ('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
         '?key={}&steamids=76561197999386785'.format(settings.STEAM))
  payload = { 'User-Agent': 'http://thingsima.de <marcus@thingsima.de>' }
  r = requests.get(url, headers=payload)
  data = r.json()
  state = data['response']['players'][0]['personastate']
  if 'gameid' in data['response']['players'][0]:
    state = 2
  social = { 'steam': state }
  return render(request, 'contact/social.html', { 'social': social })
