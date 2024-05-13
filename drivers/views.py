from django.shortcuts import render
from django.contrib import messages
from .models import Driver
from .forms import DriverForm, OperatorForm
import qrcode
from django.http import JsonResponse
import base64
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def tricycle(request):
    context = {}
    if request.method != "POST":
        driverForm = DriverForm()
        operatorForm = OperatorForm
    else:
        driverForm = DriverForm(request.POST)
        operatorForm = OperatorForm(request.POST)

        if driverForm.is_valid() and operatorForm.is_valid():
            driver = driverForm.save() 
            qr = qrcode.make(f"{driver.id}-{driver.plate_number}-{driver.rate}")
            dest = f"qr/{driver.plate_number}.png"
            qr.save(dest)


            Driver.objects.filter(id=driver.id).update(
                qr_code = dest, vhs = 2
            )
            operatorForm.save()
            
        else:
            messages.error(request, "Invalid Form")

    drivers = Driver.objects.filter(vhs=2)
    context['drivers'] = drivers
    context['driverform'] = driverForm
    context['operatorForm'] = operatorForm

    return render(request, "tricycle.html", context)

@login_required
def getQr(request):
    context = {}
    if request.method == "POST":
        id = request.POST.get("id")
        data = Driver.objects.filter(id=id)
        if data.exists():
            file_path = data[0].qr_code
            context["name"] = str(data[0])
            context['plate_number'] = data[0].plate_number
            with open(file_path, 'rb') as image_file:
                image_data = image_file.read()
                # Encode the binary data as base64 string
                base64_encoded_data = base64.b64encode(image_data).decode('utf-8')
                context["data"] = base64_encoded_data
                context["code"] = 200   
        else:
            context['code'] = 404
    else:
        context['code'] = 403

    return JsonResponse(context)

@login_required
def cab(request):
    context = {}
    if request.method != "POST":
        driverForm = DriverForm()
        operatorForm = OperatorForm
    else:
        driverForm = DriverForm(request.POST)
        operatorForm = OperatorForm(request.POST)

        if driverForm.is_valid() and operatorForm.is_valid():
            driver = driverForm.save(commit= False) 
            driver.vhs = 1

            qr = qrcode.make({"key" : f"{driver.plate_number}-{driver.rate}"})
            dest = f"qr/{driver.plate_number}.png"
            qr.save(dest)

            driver.qr_code = dest
            driver.save()
            operatorForm.save()
            
        else:
            messages.error(request, "Invalid Form")

    drivers = Driver.objects.filter(vhs=1)
    context['drivers'] = drivers
    context['driverform'] = driverForm
    context['operatorForm'] = operatorForm

    return render(request, "cab.html", context)