from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Course, CodeSnippet
from .forms import SnippetForm


def index(request):
    if request.POST:
        course_name = request.POST.get("course_name").title()
        if course_name:
            if not doesCourseExist(course_name):
                addCourse(course_name)

            return HttpResponseRedirect(reverse("codeshare:course", kwargs={"course_name": course_name}))

    return render(request, "codeshare/index.html")


def getCourseFromName(course_name):
    for course in Course.objects.all():
        if course.name == course_name:
            return course


def addSnippet(form, course_name):
    newSnippet = CodeSnippet()
    newSnippet.course = getCourseFromName(course_name)
    newSnippet.title = form.cleaned_data["title"]
    newSnippet.code = form.cleaned_data["code"]
    newSnippet.save()


def getCourseSnippets(course_name):
    return CodeSnippet.objects.filter(course=getCourseFromName(course_name))


def addCourse(course_name):
    newCourse = Course(name=course_name)
    newCourse.save()


def doesCourseExist(course_name):
    return course_name in list(Course.objects.all().values_list("name", flat=True))


def course(request, course_name):
    if request.POST:
        form = SnippetForm(request.POST)
        if form.is_valid():
            addSnippet(form, course_name)

    context = {
        "course_name": course_name,
        "form": SnippetForm(),
        "snippets": getCourseSnippets(course_name)
    }

    return render(request, "codeshare/course_website.html", context)


def delete(request, course_name, snippet_id):
    obj = get_object_or_404(CodeSnippet,
                            pk=snippet_id,
                            course=getCourseFromName(course_name))
    obj.delete()

    return HttpResponseRedirect(reverse("codeshare:course", kwargs={"course_name": course_name}))
