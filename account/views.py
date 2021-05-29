from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from account.forms import RegistrationForm, AccountAuthenticationForm
from django.contrib.auth import authenticate, login, logout


def home_view(request):
    
    return render(request, "account/home.html")


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