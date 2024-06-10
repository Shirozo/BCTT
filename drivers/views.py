from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import Driver, Operator
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
            dest = f"qr/{driver.id}.png"
            qr.save(dest)

            op = operatorForm.save()
            Driver.objects.filter(id=driver.id).update(
                qr_code = dest, vhs = 2, operator=op
            )

            messages.success(request, "New Driver Added!")
            
        else:
            messages.error(request, "Invalid Form")

    drivers = Driver.objects.filter(vhs=2)
    context['drivers'] = drivers
    context['driverform'] = driverForm
    context['header'] = "Tricycle"
    context['count'] = drivers.count()
    context['operatorForm'] = operatorForm

    return render(request, "driver.html", context)

@login_required
def getQr(request):
    context = {}
    if request.method == "POST":
        id = request.POST.get("id")
        data = Driver.objects.filter(id=id)
        if data.exists():
            file_path = data[0].qr_code

            context['first_name'] = data[0].first_name
            context['last_name'] = data[0].last_name
            context['plate_number'] = data[0].plate_number
            context['status'] = data[0].status
            context['op_first_name'] = data[0].operator.operator_first_name
            context['op_last_name'] = data[0].operator.operator_last_name
            context['address'] = data[0].operator.operator_address
            context['id'] = data[0].pk

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

# @login_required
# def cab(request):
#     context = {}
#     if request.method != "POST":
#         driverForm = DriverForm()
#         operatorForm = OperatorForm
#     else:
#         driverForm = DriverForm(request.POST)
#         operatorForm = OperatorForm(request.POST)

#         if driverForm.is_valid() and operatorForm.is_valid():
#             driver = driverForm.save() 
#             qr = qrcode.make(f"{driver.id}-{driver.plate_number}-{driver.rate}")
#             dest = f"qr/{driver.id}.png"
#             qr.save(dest)

#             op = operatorForm.save()
#             Driver.objects.filter(id=driver.id).update(
#                 qr_code = dest, vhs = 1, operator=op
#             )

#             messages.success(request, "New Driver Added!")
            
#         else:
#             messages.error(request, "Invalid Form")

#     drivers = Driver.objects.filter(vhs=1)
#     context['drivers'] = drivers
#     context['driverform'] = driverForm
#     context['header'] = "Cab"
#     context['count'] = drivers.count()
#     context['operatorForm'] = operatorForm

#     return render(request, "driver.html", context)


@login_required
def update(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            id = request.POST.get("id")

            driver_data = Driver.objects.get(id=id)

            new_driver_data = DriverForm(request.POST or None, instance=driver_data)

            operator_data = Operator.objects.get(id=driver_data.pk)

            new_op = OperatorForm(request.POST or None, instance=operator_data)

            if new_driver_data.is_valid() and new_op.is_valid():
                nd = new_driver_data.save()
                new_op.save()

                qr = qrcode.make(f"{nd.id}-{nd.plate_number}-{nd.rate}")
                dest = f"qr/{nd.id}.png"
                qr.save(dest)

                messages.success(request, "Updated Succesfully!")

            else:
                messages.error(request, "Form Validation Failed!")
            
        else:
            messages.error(request, "Access Forbidden")

    else:
        messages.error(request, "Access Denied!")
    
    past_url = request.POST.get('rdr')
    if past_url == "Cab":
        return redirect(reverse("cab"))
    return redirect(reverse("tryc"))