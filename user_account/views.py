from django.http import HttpResponse , HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserSignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.mail import send_mail


def homepage(request):
    return render(request , 'index.html')


def usersignup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(user.password)
            user.save()
            current_site = get_current_site(request)
            from_email = 'subhasispatra94@gmail.com'
            subject = 'Activate Your Account'
            message = render_to_string('activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            
            send_mail(
                    subject,
                    message,
                    from_email,
                    [to_email],
                    fail_silently=False,
                )
          
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
    else:
        form = UserSignUpForm()
    return render(request, 'signup.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('login success')
    else:
        return HttpResponse('Activation link is invalid!')