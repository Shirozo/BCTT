from django.urls import path
from . import views


urlpatterns = [
    path("", view=views.transactions, name="transac"),
    # path("reload/", view=views.reload, name="reload"),
    path("scan", view=views.scanQr, name="scan"),
    path("driver/api", view=views.driver_exist, name="driver_api"),
    path("transaction/data", view=views.transactionAPI, name="transactAPI"),
    path("transaction/no/show", view=views.noShow, name="removeshow")
]