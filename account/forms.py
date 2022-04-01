from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import models, widgets
from .models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'user_type',
                  'image', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder': 'name@mail.com'}),


            'password1': forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Confirm Password'}),
        }


class UpdateUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'image', 'about']
        widgets = {
            'first_name': widgets.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control mb-2'}),
            'last_name': widgets.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control mb-2'}),
            'about': widgets.TextInput(attrs={'placeholder': 'About', 'class': 'form-control mb-2'}),
        }
