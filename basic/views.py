from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from basic.forms import LoginForm
from django.core.context_processors import csrf
from basic.forms import RegistrationForm
from basic.models import UserProfile
from django.template import RequestContext
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def register_user(request):
    args = {}
    args.update(csrf(request))
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        args['form'] = form
        if form.is_valid():
            form.save()  # save user to database if form is valid
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            mobile_number = form.cleaned_data['mobile_number']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt + email).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(7)

            # Get user by username
            user = User.objects.get(username=username)

            # Create and save user
            new_profile = UserProfile(user=user, activation_key=activation_key,
                                      key_expires=key_expires,
                                      mobile_number=mobile_number)
            new_profile.save()
            print("Saved")
            # Send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            7days http://localhost:8000/accounts/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'artdiscern@gmail.com',
                      [email], fail_silently=False)

            return HttpResponseRedirect('/register_success')
    else:
        print("THis is a GET")
        args['form'] = RegistrationForm()

    return render_to_response('register.html', args, context_instance=RequestContext(request))


def custom_login(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        args['form'] = form
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            print("got the email")
            user_name = user.username
            password = form.cleaned_data['password']
            user = authenticate(username=user_name, password=password)
            if user is not None:
                print("User is not none")
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/home')
                else:
                    return HttpResponseRedirect("/inactive")

    else:
        if request.user.is_authenticated():
            HttpResponseRedirect('/home')
        args['form'] = LoginForm()

    return render_to_response('login.html', args, context_instance=RequestContext(request))


def custom_logout(request):
    logout(request)
    return render_to_response('home.html')


def home_page(request):
    return render_to_response('home.html')


def inactive(request):
    print("inactive")
    return render_to_response('inactive.html')


def register_confirm(request, activation_key):
    # check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    # check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        return render_to_response('user_profiles/confirm_expired.html')
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('user_profiles/confirm.html')


