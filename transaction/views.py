from django.shortcuts import render
from .forms import TransactionForm
from django.contrib import messages
from drivers.models import Driver
from .models import Transaction, DriverScan
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def reload(request):
    context = {}
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            data = form.save()
            id = data.driver.id

            past_balance = Driver.objects.get(id=id).balance
            
            Driver.objects.filter(id=id).update(
                balance = past_balance + data.amount
            )

            messages.success(request, f"Added Balance to {data.driver}!")
        else:
            messages.error(request, "Invalid Form!")
    else:
        reload_form = TransactionForm()
        context['reload_form'] = reload_form
    
    transact_hstry = Transaction.objects.all()
    context['hstry'] = transact_hstry
    return render(request, "reload.html", context)


def scanQr(request):
    context = {}
    data = request.GET.get("data")
    id, plate_number, rate = data.split("-")
    
    has_data = Driver.objects.filter(id=id, plate_number=plate_number)

    if has_data.exists():
        
        driver_data = has_data[0]

        if driver_data.balance >= int(rate):
            transact_detail = DriverScan(driver=driver_data, amount=rate)
            transact_detail.save()

            has_data.update(balance = driver_data.balance - int(rate))
            context['code'] = 200
            context['message'] = "Transaction Success!"
        else:
            context['code'] = 403
            context['message'] = "Insufficient Balance!"
    else:
        context['code'] = 404
        context["message"] = "Driver Details not Found"

    return JsonResponse(context)

@login_required
def transactions(request):
    transact = DriverScan.objects.all()
    context = {
        "transact" : transact
    }
    return render(request, "transaction.html", context)