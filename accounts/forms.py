from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
        labels = {
            'username': ' שם משתמש',
            'email': ' אימייל',
            'phone_number': ' טלפון',
        }
        help_texts = {field: '' for field in fields}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # תרגום שדות הסיסמה
        self.fields['password1'].label = ' סיסמה'
        self.fields['password2'].label = ' אימות סיסמה'

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
