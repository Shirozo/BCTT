from django import forms
from .models import Driver, Operator

class FormSetting(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSetting, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class DriverForm(FormSetting):
    class Meta:
        model = Driver
        fields = [
            "first_name",
            "last_name",
            "plate_number",
            "rate"
        ]

class OperatorForm(FormSetting):
    class Meta:
        model = Operator
        fields = [
            "first_name",
            "last_name",
            "address"
        ]