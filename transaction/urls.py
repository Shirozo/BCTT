from django.urls import path
from . import views


urlpatterns = [
    path("", view=views.transactions, name="transac"),
    path("reload/", view=views.reload, name="reload"),
    path("scan/", view=views.scanQr, name="scan")
]