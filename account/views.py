from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegisterForm
from .models import CustomUser

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

def registerUser(request):
    
    if request.method == "POST":
        rForm = RegisterForm(request.POST)
        if rForm.is_valid():
            rForm.save()
            messages.success(request, "New Staff Created")
            rForm = RegisterForm()
        else:
            messages.error(request, "Invalid Form!")
    else:
        rForm = RegisterForm()
    huser = CustomUser.objects.all()
    
    return render(request, "register.html", context={
        "rForm" : rForm,
        "huser" : huser,
        "userCount" : huser.count()
    })
    

def delete(request):
    if request.method == "POST":
        id = request.POST.get("r_staff_id")
        
        if not id: 
            messages.error(request, "Action Forbidden!")
        else:
            data = CustomUser.objects.get(id=id)
            data.delete()
            messages.success(request, "Staff Removed!")
    else:
        messages.error(request, "Action Forbidden!")
    
    return redirect(reverse("register"))

def update(request):
    pass