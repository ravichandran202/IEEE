from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


import random
#send email to newly created user
def account_created_email(new_user_data, user_password):
    subject = 'noreply - Request Successfully Completed'
    
    context = {
        'new_user_data' : new_user_data,
        'user_password' : user_password
    }

    
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [new_user_data.email]
    html_message = render_to_string('email-pages/account-created-email.html',context=context)
    message = strip_tags(html_message)
    
    try:
        send_mail( subject, message, email_from, recipient_list ,html_message=html_message)
    except:
        pass
    
def announcement_email(title,content):
    subject = 'Announcement'
    
    context = {
        'title' : title,
        'content' : content
    }

    
    email_from = settings.EMAIL_HOST_USER
    recipient_list = []
    for user in User.objects.all():
        recipient_list.append(user.email)
    html_message = render_to_string('email-pages/announce-email.html',context=context)
    message = strip_tags(html_message)
    
    try:
        send_mail( subject, message, email_from, recipient_list ,html_message=html_message)
    except:
        pass

#used to generate random password to new user
def generate_password():
    english_alphabets = [ chr(i).lower() for i in range(64,91)]
    random.shuffle(english_alphabets)
    return "".join(english_alphabets[:9])


# Create your views here.
'''
Authentication Pages
'''
def register_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['email'][:-10]  # removes '@gmail.com' suffix
        password = generate_password()
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Exists")
            return redirect('register_page')
        else:
            user = User.objects.create_user(username, email, password)
            user.save()
            messages.info(request, "check your email for Username and Password")
            
            account_created_email(user,password)
            
            return redirect('login_page')
    return render(request,"register-page.html")

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("home_page")
        else:
            messages.error(request, 'Username or Password is incorrect')
            return redirect("login_page")
    return render(request,"login-page.html")


def home_page(request):
    return render(request,"home.html")


@login_required(login_url='login_page')
def logout(request):
    auth.logout(request)
    return redirect('login_page')

def forgot_password_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            new_password = generate_password()
            user.set_password(new_password)
            user.save()
            account_created_email(user, new_password)
            messages.info(request, 'Username or Password is sent to your email')
            return redirect("login_page")
        else:
            messages.error(request, "Email is not Exists")
            return redirect('forgot_password')
    return render(request,"forgot-password.html")

def contact_page(request):
    return render(request,"contact.html")

def about_page(request):
    return render(request,"about.html")

def pricing_page(request):
    return render(request,"pricing.html")

def faq_page(request):
    return render(request,"faq.html")

def vendors_page(request):
    return render(request,"vendors.html")

def vendor_page(request,id):
    return render(request,"vendor.html")

def announce_page(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        announcement_email(title,content)
    return render(request,"announce_page.html")