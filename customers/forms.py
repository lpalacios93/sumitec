from django import forms

from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "customer_type",
            "name",
            "phone",
            "whatsapp",
            "email",
            "address",
            "ruc",
            "notes",
        ]
        widgets = {
            "customer_type": forms.Select(),
            "name": forms.TextInput(attrs={"autofocus": True}),
            "phone": forms.TextInput(),
            "whatsapp": forms.TextInput(),
            "email": forms.EmailInput(),
            "address": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }
