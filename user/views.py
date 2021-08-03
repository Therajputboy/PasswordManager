from safe.utils import decrypt_password
from user.models import AuthToken
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
import uuid
from django.conf import settings
from .models import AuthToken,Profile
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import hashlib
from safe.models import Safe 
from safe.utils import *
# Create your views here.


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Welcome to the Password Manager. Strore all your personal \
                credentials with full security in this system. We store your passwords in encrypted form and even site owner \
                    cannot decrypt your data.")
            return redirect('home')
        else:
            messages.warning(request,"Credentials didn't match any account.")
    return render(request,'user/login.html',{'title':'Login'})


def register(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            check_username = User.objects.filter(username=username)
            if check_username.exists():
                messages.warning(request,'Username already exist. ')
                return redirect('register')
            check_email = User.objects.filter(email=email)
            if check_email.exists():
                messages.warning(request,'Email already register with a user. ')
                return redirect('register')
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 != password2:
                messages.warning(request,'Both passwords should match. ')
                return redirect('register')
            user = User(username=username,email=email,is_active=False)
            user.set_password(password1)
            user.save()
            token = str(uuid.uuid1())
            AuthToken.objects.create(user=user,auth_token=token)
            url = settings.DOMAIN_NAME + 'account-activate/' + token
            subject = "Activate account"
            message = "Hi " + username + ",<br/>" + "Please click on the below activation link to activate your account.<br/>" \
                                                            + url
            email_from = settings.EMAIL_HOST_USER
            recepient=[email,]
            send_mail(subject,"",email_from,recepient,html_message=message,fail_silently = False)
            messages.success(request,'User created successfully. We have sent you a mail to activate the user.')
            return redirect('login')
        except Exception as e:
            messages.warning(request,str(e) + 'Try after some time.')
            User.objects.filter(username = username).delete()
            return redirect('register')
    return render(request,'user/register.html',{'title':'Register'})

def account_activate(request,token):
	try:
		auth_token_obj =AuthToken.objects.get(auth_token=token)
	except AuthToken.DoesNotExist:
		messages.warning(request,'User does not exist, wrong url')
		return HttpResponse('403 Forbidden')
	auth_token_obj.user.is_active = True 
	auth_token_obj.user.save()
	return render(request,'user/account_activate.html')

def logout_view(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect('login')

def reset_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        user_list = User.objects.filter(username=username)
        if user_list.exists():
            user = user_list[0]
            email = user.email
            token = str(uuid.uuid1())
            auth_token_obj = AuthToken.objects.get(user=user)
            auth_token_obj.auth_token = token
            auth_token_obj.save()
            url = settings.DOMAIN_NAME + 'reset-password-confirm/' + token
            subject = "Reset Password"
            message = "Hi " + username + ",<br/>" + "Please click on the below  link to reset your account password.<br/>" \
                                                            + url
            email_from = settings.EMAIL_HOST_USER
            recepient=[email,]
            send_mail(subject,"",email_from,recepient,html_message=message,fail_silently = False)
            messages.success(request,'We have sent a mail to the registered email id. Please reset from there.')
            return redirect('login')
        else:
            messages.warning(request,'User does not exist')
    return render(request,'user/reset_password.html')

def reset_password_confirm(request,token):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 =request.POST['password2']
        if password1 != password2:
            messages.warning(request,'Both the passwords should match.')
            return redirect('reset-password-confirm')
        else:
            try:
                auth_token_obj = AuthToken.objects.get(auth_token=token)
            except AuthToken.DoesNotExist:
                return HttpResponse('<h1>403 Forbidden</h1>')
            user = auth_token_obj.user
            user.set_password(password1)
            user.save()
            messages.success(request,'Password successfully changed.')
            return render(request,'user/reset_password_done.html')

    return render(request,'user/reset_password_confirm.html')
@login_required
def profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if profile.master_key == "":
        action = "Create"
    else:
        action = "Update"
    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()
        if 'profile_image' in request.FILES.keys():
            profile.image = request.FILES['profile_image']
            profile.save()
    return render(request,'user/profile.html',{'profile':profile,'action':action})

@login_required
def master_key(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if profile.master_key == "":
        action = "Create"
    else:
        action = "Update"
    if request.method == "POST":
        master_key1 = request.POST['master_key1']
        master_key2 = request.POST['master_key2']
        print(master_key1,master_key2)
        if master_key1 != master_key2:
            messages.warning(request,"Both master keys should match.")
            return redirect('master-key')
        if action == "Update":
            old_master_key = request.POST['old_master_key']
            md5_master_key = hashlib.md5(request.POST['old_master_key'].encode()).hexdigest()
            if profile.master_key != md5_master_key:
                messages.warning(request,"Enter correct old master key to update your master key.")
                return redirect('master-key')
            else:
                sites = Safe.objects.filter(user = request.user)
                for site in sites:
                    decrypted_password = decrypt_password(site.site_password,old_master_key)
                    new_encrypted_password = encrypt_password(decrypted_password,master_key1)
                    site.site_password = new_encrypted_password
                    site.save()
        profile.master_key = hashlib.md5(master_key1.encode()).hexdigest()
        profile.save()
        messages.success(request,f'Master key {action} successully')
        return redirect('profile')
    return render(request,'user/master.html',{'action':action})

    