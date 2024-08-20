from django.shortcuts import render, redirect, reverse
# from .forms import TransactionForm-
from django.contrib import messages
from drivers.models import Driver
from .models import Transaction, DriverScan
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from datetime import datetime, date
# Create your views here.

# @login_required
# def reload(request):
#     context = {}
#     if request.method == "POST":
#         form = TransactionForm(request.POST)
#         if form.is_valid():
#             data = form.save()
#             id = data.driver.id

#             past_balance = Driver.objects.get(id=id).balance
            
#             Driver.objects.filter(id=id).update(
#                 balance = past_balance + data.amount
#             )

#             messages.success(request, f"Added Balance to {data.driver}!")
#         else:
#             messages.error(request, "Invalid Form!")
#     else:
#         reload_form = TransactionForm()
#         context['reload_form'] = reload_form
    
#     transact_hstry = Transaction.objects.all()
#     context['hstry'] = transact_hstry
#     return render(request, "reload.html", context)


@login_required
def scanQr(request):
    context = {}
    data = request.GET.get("data")
    designation = request.GET.get("designation")
    action = request.GET.get("b_action")
    try:
        id, plate_number = data.split("-")
    except Exception:
        context['code'] = 500
        context['message'] = "Invalid QR Code!"
    else:
        
        if designation == "1":
            endpoint = "Merkado"
        
        elif designation == "2":
            endpoint = "Pepelitan"
        else:
            context["code"] = 403
            context['message'] = "Action Forbidden"
            return JsonResponse(context)
        
        has_data = Driver.objects.filter(id=id, plate_number=plate_number)

        context["action"] = action
                
        if has_data.exists():
            
            driver_data = has_data[0]

            if action.strip() == "pay":
                if driver_data.status == "unpaid":
                    transact_detail = DriverScan(driver=driver_data, endpoint=endpoint, action="Pay")
                    transact_detail.save()

                    has_data.update(status = "paid")
                    context['id'] = transact_detail.pk
                    context['code'] = 200
                    context['plate_number'] = driver_data.plate_number
                    context["endpoint"] = endpoint
                    context['message'] = "Transaction Success!"
                else:
                    context['code'] = 403
                    context['message'] = "Already scanned!"

            
            elif action.strip() == "pass":
                if driver_data.status == "paid":
                    transact_detail = DriverScan(driver=driver_data, endpoint=endpoint, action="Scanned")
                    transact_detail.save()

                    has_data.update(status = "unpaid")
                    context['id'] = transact_detail.pk
                    context['code'] = 200
                    context['plate_number'] = driver_data.plate_number
                    context["endpoint"] = endpoint
                    context['message'] = "Transaction Success!"
                else:
                    context['code'] = 403
                    context['message'] = "Driver didn't pay!"
                    
            elif action.strip() == "pay_pass":
                if driver_data.status != "paid":
                    pay_detail = DriverScan(driver=driver_data, endpoint="Pepelitan", action="Pay")
                    pay_detail.save()
                
                    scan_detail = DriverScan(driver=driver_data, endpoint=endpoint, action="Scanned")
                    scan_detail.save()
                    
                    context['id'] = pay_detail.pk
                    context['code'] = 200
                    context['plate_number'] = driver_data.plate_number
                    context["endpoint"] = "Pepelitan"
                    context["action"] = "Paid"
                    context['message'] = "Driver Paid!"
                else:
                    context['code'] = 403
                    context['message'] = "Driver Already Paid!"
                
            else:
                context['code'] = 404
                context["message"] = "Invalid Action!"

        else:
            context['code'] = 404
            context["message"] = "Driver Details not Found"


    return JsonResponse(context)

@login_required
def transactions(request):
    today = date.today()

    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())
    if request.user.designation == 1: 
        transact = DriverScan.objects.filter(
            scanDate__range=(start_of_day, end_of_day),
            action="Pay"
        )
    else:
        transact = DriverScan.objects.filter(
            scanDate__range=(start_of_day, end_of_day),
            endpoint="merkado"
        ).filter(show = 1)
    
    if request.user.is_superuser:
        transact = DriverScan.objects.all()
        
    context = {
        "transact" : transact,
        "count" : transact.count(),
    }
    return render(request, "transaction.html", context)

def driver_exist(request):
    context = {}
    qr = request.GET.get("qr")
    try:
        id, plate_number = qr.split("-")
    except Exception:
        context["code"] = 403
    else:
        data = Driver.objects.filter(plate_number=plate_number).filter(id=id)
            
        if data.exists and len(data) > 0:
            context["code"] = 200
        else:
            context["code"] = 403
            
    return JsonResponse(context)

def transactionAPI(request):
    id = request.GET.get("id")
    
    data = DriverScan.objects.get(id=id)
    
    context = {
        "body_number" : data.driver.plate_number,
        "endpoint" : data.endpoint,
        "action" : data.action,
        "date" : data.scanDate
    }
    
    return JsonResponse(context)

def noShow(request):
    p_number = request.GET.get("id")
    
    data = DriverScan.objects.filter(driver__plate_number = p_number).filter(show=1)
    
    data.update(show=False)
    
    return JsonResponse({"message" : "remove"})