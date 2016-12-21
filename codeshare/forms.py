from django import forms

from django.forms import TextInput, Textarea
from django.contrib.auth.models import User

from .models import Instructor, CodeSnippet


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'name': 'password', 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = [
            "username",
            "password",
        ]
        widgets = {
            "username": TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder': 'Username', 'autocomplete': 'off'}),
        }


class InstructorForm(forms.ModelForm):

    class Meta:
        model = Instructor
        fields = []


class SnippetForm(forms.ModelForm):

    class Meta:
        model = CodeSnippet
        fields = [
            "title",
            "code",
        ]
        widgets = {
            "title": TextInput(attrs={'class': 'form-control', 'placeholder': 'Title (not required)'}),
            "code": Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter code here'}),
        }
