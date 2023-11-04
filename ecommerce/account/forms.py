from django import forms
from typing import Any

# django's built-in default user creation form
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.forms.widgets import PasswordInput, TextInput

# using django's built-in User model
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    """ User Registration form"""
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    # we want to have access to fields defined under Meta class, we want to modify those fields 
    # and gain access to them as we wish
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        # make email field required beacuse by default in User model email field is not required
        self.fields['email'].required = True

    # by defalut django has inbuilt validation for username that is no 2 can have same username
    # we are defining validation for email field
    def clean_email(self):
        """ email validation"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is invalid.')
        if len(email) >= 350:
            raise forms.ValidationError('Email is too long.')
        return email


class LoginForm(AuthenticationForm):
    """ User Login Form"""
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())



class UpdateUserForm(forms.ModelForm):
    """ updating user's username and email """
    password = None             # we are not updating password so we are explicitly seting it None
    class Meta:
        model = User
        fields = ['username', 'email']
        exclude = ['password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        
    def clean_email(self):
        """ email validation """
        email = self.cleaned_data.get('email')
        # exclude email of current user who is  logged in based on his primary key
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Email is invalid.')
        if len(email) >= 350:
            raise forms.ValidationError('Email is too long.')
        return email


