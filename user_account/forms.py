from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserSignUpForm(forms.ModelForm):
    email = forms.EmailField(max_length=100, help_text='Required')
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password')