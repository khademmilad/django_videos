from django.contrib.auth import authenticate
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from account.forms import RegistrationForm
from django.contrib.auth import login


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
