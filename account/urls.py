from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("", view=views.registerUser, name="register"),
    path("delete/", view=views.delete, name="delete"),
    path("update/", view=views.update, name="update")
]