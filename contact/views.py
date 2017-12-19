from django.core.mail import send_mail
from django.shortcuts import render
import requests

def contact(request):
  if request.method == 'POST':
    payload = { 'secret': '6LdtITYUAAAAAA-iThAoHjgAacMux1ge6g1G4ulg', 'response': request.POST['g-recaptcha-response'] }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
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
    if validity:
      return render(request, 'contact/success.html')
    else:
      return render(request, 'contact/robot.html')
  return render(request, 'contact/form.html')
