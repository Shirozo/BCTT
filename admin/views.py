from django.shortcuts import render, redirect, reverse

# Create your views here.

def home(request):
    return redirect(reverse("reload"))
