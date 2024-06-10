from django.shortcuts import render, redirect, reverse
# from .forms import TransactionForm-
from django.contrib import messages
from drivers.models import Driver
from .models import Transaction, DriverScan
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
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
    action = request.GET.get("action")
    try:
        id, plate_number, _ = data.split("-")
        endpoint = request.GET.get("endpoint")
    except Exception:
        context['code'] = 500
        context['message'] = "Invalid QR Code!"
        messages.error(request, "Invalid QR Code!")
    else:
        
        if not endpoint:
            context["code"] = 405
            context["message"] = "Invalid QR Code!"
            messages.error(request, "Invalid QR Code!")
        
        else:
            has_data = Driver.objects.filter(id=id, plate_number=plate_number)

            
            if has_data.exists():
                
                driver_data = has_data[0]

                if action.strip() == "pay":
                    if driver_data.status == "unpaid":
                        transact_detail = DriverScan(driver=driver_data, action="Pay")
                        transact_detail.save()

                        has_data.update(status = "paid")
                        context['code'] = 200
                        context['plate_number'] = driver_data.plate_number
                        context['message'] = "Transaction Success!"
                        messages.success(request, "Transaction Success!")
                    else:
                        context['code'] = 403
                        context['message'] = "Already scanned!"
                        messages.error(request, "Already scanned!")
                
                elif action.strip() == "pass":
                    if driver_data.status == "paid":
                        transact_detail = DriverScan(driver=driver_data, endpoint=endpoint, action="Scanned")
                        transact_detail.save()

                        has_data.update(status = "unpaid")
                        context['code'] = 200
                        context['plate_number'] = driver_data.plate_number
                        context['message'] = "Transaction Success!"
                        messages.success(request, "Transaction Success!")
                    else:
                        context['code'] = 403
                        context['message'] = "Driver didn't pay!"
                        messages.error(request, "Driver didn't pay!")
                
                else:
                    context['code'] = 404
                    context["message"] = "Driver Details not Found"
                    messages.error(request, "Driver Details not Found")

            else:
                context['code'] = 404
                context["message"] = "Driver Details not Found"
                messages.error(request, "Driver Details not Found")


    return redirect(reverse("transac"))

@login_required
def transactions(request):
    transact = DriverScan.objects.all()
    context = {
        "transact" : transact,
        "count" : transact.count(),
    }
    return render(request, "transaction.html", context)