from django.conf import settings
from django.shortcuts import render
import requests

def contact(request):
  render(request, 'contact/form.html')
  try:
    name = request.POST['name']
    email = request.POST['email']
    message = request.POST['message']
    captcha = request.POST['g-recaptcha-response']

    if not captcha:
      print('please complete the captcha')
      return render(request, 'contact/form.html')
    
    if not message:
      please('please enter a message')
      return render(request, 'contact/form.html')

    url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {
        'secret': settings.RECAPTCHA,
        'response': captcha
    }
    r = requests.post(url, data=payload)
    response = r.json()

    if response['success']:
      return render(request, 'contact/success.html')
    else:
      return render(request, 'contact/form.html')
  except Exception as error:
    print('something broke', error)
    return render(request, 'contact/form.html')
