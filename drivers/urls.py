from django.urls import path
from . import views

urlpatterns = [
    path('tricycle/', view=views.tricycle, name="tryc"),
    path("update/", view=views.update, name="update"),
    path("getqr", view=views.getQr, name='getQr'),
    # path("cab/", view=views.cab, name="cab")X
]
