from video.models import Subscriber, Video
from django.http import request
from account.models import Account
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core import files


def home_view(request):
    
    return render(request, "account/home.html")


def profile_view(request, *args, **kwargs):
    context = {}
    user_id = kwargs.get('user_id')
    profile_to_subscribe = Subscriber.objects.get_or_create(user=Account.objects.get(id=user_id))[0]
  
    try:
        account = Account.objects.get(pk=user_id)
    except:
        return HttpResponse('Somthing went wrong!')
        
    if account:   
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image'] = account.profile_image
        
        is_self = True
        user = request.user
        
        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False
            
        context['is_self'] = is_self
    
    subscribed = False
    if request.user in profile_to_subscribe.subscribers.all():
        subscribed = True
    else:
        subscribed = False
    
    count_subs = profile_to_subscribe.subscribers.all().count()
    
    context['subscribed'] = subscribed
    context['count_subs'] = count_subs
    
    count_videos = Video.objects.filter(user = account).count()
    context['count_videos'] = count_videos
    
    return render(request, 'account/profile.html', context)



def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticate as " + str(user.email))
    dic = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email = email, password = raw_password)
            login(request, account)
            go_to_page = kwargs.get('next')
            if go_to_page:
                return redirect(go_to_page)
            return redirect('account:account_home')
        else:
            dic['form'] = form
    
    else:
        form = RegistrationForm()
        dic['form'] = form
        
    return render(request, 'account/register.html', dic)



def login_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return redirect('account:account_home')
    
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(email = email, password = raw_password)
            
            if user:
                login(request, user)
                return redirect('account:account_home')
    
    else:
        form = AccountAuthenticationForm()
    
    dic = {
        "login_form" : form
    }
    return render(request, "account/login.html", dic)
    
    
    
def logout_view(request):
    logout(request)
    return redirect('account:account_home')
    

def edit_account_view(request, *args, **kwrags):
    if not request.user.is_authenticated:
        return redirect('account:login')
    user_id = kwrags.get('user_id')
    account = Account.objects.get(pk=user_id)
    
    if account.pk != request.user.pk:
        return HttpResponse("You cannot edit this profile")
    dic = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account:account_home')
        else:
            form = AccountUpdateForm(request.POST, instance=request.user,
            initial={
                'id' : account.id,
                'email' : account.email,
                'username' : account.username,
                'profile_image' : account.profile_image,
                'hide_email' : account.hide_email
            }
            )
            dic['form'] = form
    else:
        form = AccountUpdateForm(
            initial={
                'id' : account.id,
                'email' : account.email,
                'username' : account.username,
                'profile_image' : account.profile_image,
                'hide_email' : account.hide_email
            }           
        )
        dic['form'] = form
        
    dic['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, 'account/edit_profile_account.html',dic)
    