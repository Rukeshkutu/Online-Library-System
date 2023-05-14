from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.urls import reverse

# for reset password
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


# Create your views here.
def admin_dashboard(request):
    return render(request, 'auth_users/admin_dashboard.html')


def user_dashboard(request):
    return render(request, 'auth_users/user_dashboard.html')


def dashboard(request):
    if request.user.is_superuser:
        return redirect('auth_users:admin_dashboard')
    else:
        return redirect('auth_users:user_dashboard')


def signin_page(request):
    if request.method == 'POST':
        username = request.POST.get(
            'username')  # here username should be same as the  "name = 'username '" in signin.html
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)  # 'username = username' is to make sure user exite

        except:
            messages.error(request, '')  # flash messages

        user = authenticate(request, username=username,
                            password=password)  # to authenticate and to make sure user is currect
        if user is not None:
            login(request, user)
            return redirect(
                'auth_users:dashboard')  # when user is login page is redirectd to home.html page through url
        else:
            messages.error(request, 'user name or email doesnot exist')

    else:
        messages.error(request, '')
    context = {

    }
    return render(request, 'auth_users/signin.html', context)


def signout_page(request):
    logout(request)  # this delete the token so it delete the user
    return redirect("books:digital_books")


def register_page(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # email = form.cleaned_data.gat('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username,  password=raw_password)
            login(request, user)
            messages.success(request, 'user created successfully')
            return redirect('auth_users:signin_page')
    else:
        form = SignUpForm()

    context = {
        'form': form
    }
    return render(request, 'auth_users/register.html', context)

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "auth_users/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        "domain": '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

                    messages.success(request, '')
                    return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()

    context = {
        'password_reset_form': password_reset_form,
    }
    return render(request, "auth_users/password_reset.html", context)