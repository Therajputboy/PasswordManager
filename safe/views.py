from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import hashlib
from user.models import Profile
from .models import Safe
from django.contrib import messages
from .utils import *
from django.db.models import Q

# Create your views here.
@login_required
def home(request):
    try:
        sites = Safe.objects.filter(user=request.user)
        return render(request,'safe/home.html',{'sites':sites})
    except Safe.DoesNotExist:
        messages.success(request,'No password added yet.')
        #return redirect('home')
    return render(request,'safe/home.html')

@login_required
def add_password(request):
    profile = Profile.objects.get(user = request.user)
    if profile.master_key == "":
        messages.info(request,"Please create your master key by going to the profile section then add password.")
        return redirect('home')
    if request.method == 'POST':
        site_name = request.POST['site_name']
        site_url = request.POST['site_url']
        site_text = request.POST['site_text']
        site_username = request.POST['site_username']
        site_password = request.POST['site_password']
        master_key = request.POST['master_key']
        md5_master_key = hashlib.md5(request.POST['master_key'].encode()).hexdigest()
        profile = Profile.objects.get(user=request.user)
        print(profile.master_key,md5_master_key)
        if profile.master_key != md5_master_key:
            messages.warning(request,'Wrong master key')
            return redirect('add-password')
        else:
            password = encrypt_password(site_password,master_key)
            Safe.objects.create(user=request.user,site_name=site_name,site_url=site_url,site_text=site_text,site_username=site_username,site_password=password)
            messages.success(request,f'Password added successfully for {site_name}')
            return redirect('home')
    return render(request,'safe/add_password.html')
@login_required
def show_password(request,id):
    site = Safe.objects.get(Q(id=id) & Q(user=request.user))
    if request.method == 'POST':
        master_key = request.POST['master_key']
        profile = Profile.objects.get(user = request.user)
        md5_master_key = hashlib.md5(master_key.encode()).hexdigest()
        if md5_master_key != profile.master_key:
            messages.warning(request,'Wrong master key')
            return redirect('show-password',id=id)
        else:
            decrypted_password = decrypt_password(site.site_password,master_key)
            return render(request,'safe/show_password.html',{'site':site,'decrypted_password':decrypted_password})
    return render(request,'safe/show_password.html',{'site':site})

@login_required
def delete_password(request,id):
    site = Safe.objects.get(Q(id=id)&Q(user=request.user))
    if request.method == 'POST':
        messages.success(request,f'Password for {site.site_name} deleted successfully')
        site.delete()
        return redirect('home')
    return render(request,'safe/delete_password.html',{'site':site})

@login_required
def update_password(request,id):
    site = Safe.objects.get(Q(id=id)&Q(user=request.user))
    if request.method == 'POST':
        master_key = request.POST['master_key']
        md5_master_key = hashlib.md5(request.POST['master_key'].encode()).hexdigest()
        profile = Profile.objects.get(user=request.user)
        if profile.master_key != md5_master_key:
            messages.warning(request,'Wrong master key')
            return redirect('update-password')
        else:
            site.site_name = request.POST['site_name']
            site.site_url = request.POST['site_url']
            site.site_text = request.POST['site_text']
            site.site_username = request.POST['site_username']
            site_password = request.POST['site_password']
            password = encrypt_password(site_password,master_key)
            site.site_password = password
            site.save()
            messages.success(request,f'Password updated successfully for {site.site_name}')
            return redirect('home')
    return render(request,'safe/update_password.html',{'site':site})


