from dataclasses import fields
from django import forms
from .models import Profile
from django.contrib.auth.forms import UserChangeForm


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email =  forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ('gender', 'date_of_birth', 'credit', 'photo')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'date_of_birth', 'credit', 'photo']


class UserEditForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = ('username', 'first_name', 'last_name', 'email')
    password = None
