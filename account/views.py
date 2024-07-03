from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

# Create your views here.
def loginPage(request):
    if request.user.is_authenticated:
        return redirect(reverse("transac"))
    else:

        if request.method == "POST":

            forms  = AuthenticationForm(request,request.POST)
            print(forms)
            username = forms.cleaned_data.get("username")
            password = forms.cleaned_data.get("password")
            print(password)
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Welcome!")
                return redirect(reverse("transac"))
            messages.error(request, "Invalid Username or Password!")
        else:
            forms = AuthenticationForm()
        
        return render(request, "login.html", context={"forms" : forms})


def logoutPage(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request, "Logged Out!")
    else:
        messages.error(request, "You are not logged In!")
    

    return redirect(reverse("login"))
