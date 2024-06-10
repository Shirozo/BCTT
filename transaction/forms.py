from django import forms
from drivers.forms import FormSetting
from .models import Transaction

# class TransactionForm(FormSetting):
#     class Meta:
#         model = Transaction
#         fields = [
#             "driver",
#             "amount"
#         ]