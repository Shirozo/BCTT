from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    
    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2", "designation"]
        widgets = {
            "designation" : forms.Select(attrs={
                "class" : "form-control"
            }),
        }