from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
import requests

def contact(request):
  if request.method == 'POST':
    payload = { 'secret': settings.RECAPTCHA_PRIVATE,
                'response': request.POST['g-recaptcha-response'] }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    # Is the user a robot or not? Either way, we'll accept their submission
    validity = r.json()['success']
    name = request.POST['name']
    email = request.POST['email']
    message = request.POST['message']
    msg = 'Name: {}\nEmail: {}\nMessage: {}'.format(name, email, message)
    send_mail(
      'Mail from site | Valid: {}'.format(validity),
      msg,
      email,
      ['marcus@thingsima.de'],
      fail_silently=False,
    )
    # If they're a user, say thanks otherwise as a joke, render a thanks robot page
    if validity:
      return render(request, 'contact/success.html')
    else:
      return render(request, 'contact/robot.html')
  contact = { 'recaptcha': settings.RECAPTCHA_PUBLIC }
  return render(request, 'contact/form.html', { 'contact': contact })
