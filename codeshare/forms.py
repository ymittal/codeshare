from django import forms

from django.forms import TextInput, Textarea

from .models import CodeSnippet


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
