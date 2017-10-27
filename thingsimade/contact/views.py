from django.shortcuts import render

def contact(request):
  render(request, 'contact/form.html')
  try:
    name = request.POST['name']
    email = request.POST['email']
    message = request.POST['message']
    captcha = request.POST['g-recaptcha-response']
    print(name, email, message, captcha)

    if not captcha:
      print('please do captcha')
      return render(request, 'contact/form.html')
    
    if not message:
      please('please enter a message')
      return render(request, 'contact/form.html')

    print('success')
    return render(request, 'contact/form.html')
  except Exception as error:
    print('something broke', error)
    return render(request, 'contact/form.html')
