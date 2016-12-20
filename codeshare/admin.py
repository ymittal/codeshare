from django.contrib import admin

from .models import Instructor, Course, CodeSnippet

admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(CodeSnippet)
