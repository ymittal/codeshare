from django.contrib import admin

from .models import Course, CodeSnippet

admin.site.register(Course)
admin.site.register(CodeSnippet)
