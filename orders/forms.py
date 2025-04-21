from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer_name', 'phone_number', 'address',
            'model', 'description',
            'total_price', 'deposit_paid',
            'measure'
        ]
        labels = {
            'customer_name': 'שם לקוח',
            'phone_number': 'מספר טלפון',
            'address': 'כתובת לקוח',
            'model': 'דגם',
            'description': 'תיאור',
            'total_price': 'סכום לתשלום',
            'deposit_paid': 'מקדמה ששולמה',
            'measure': 'מדידה',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
