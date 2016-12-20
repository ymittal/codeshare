from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import authenticate

from .models import User, Course, CodeSnippet, Instructor
from .forms import SnippetForm, UserForm, InstructorForm


def index(request):
    if request.POST:
        course_name = request.POST.get("course_name").title()
        if course_name:
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


def addCourse(request, course_name):
    newCourse = Course(name=course_name)
    try:
        newCourse.creator = User.objects.get(username=request.user.username)
    except:
        newCourse.creator = User.objects.get(username='admin')
    newCourse.save()


def doesCourseExist(course_name):
    return course_name in list(Course.objects.all().values_list("name", flat=True))


def getCourseAccess(request, course_name):
    course = getCourseFromName(course_name)
    try:
        if course.creator == User.objects.get(username=request.user.username):
            return True
        else:
            return not course.isPrivate
    except:
        if course.isPrivate:
            return False
        else:
            return True


def course(request, course_name):
    if not doesCourseExist(course_name):
        addCourse(request, course_name)

    if request.POST:
        form = SnippetForm(request.POST)
        if form.is_valid():
            course_name = course_name if len(course_name) else "Code Snippet"
            addSnippet(form, course_name)

    context = {
        "course_name": course_name,
        "form": SnippetForm(),
        "snippets": getCourseSnippets(course_name),
        "can_modify": getCourseAccess(request, course_name),
    }
    
    return render(request, "codeshare/course_website.html", context)


def delete(request, course_name, snippet_id):
    obj = get_object_or_404(CodeSnippet,
                            pk=snippet_id,
                            course=getCourseFromName(course_name))
    obj.delete()

    return HttpResponseRedirect(reverse("codeshare:course", kwargs={"course_name": course_name}))


def login(request):
    if request.POST:
        if 'login' in request.POST:
            return loginUser(request)
        elif 'register' in request.POST:
            return register(request)

    context = {
        "user_form": UserForm(),
        "instructor_form": InstructorForm(),
    }

    return render(request, "codeshare/login.html", context)


def loginUser(request):
    username = request.POST['username']
    password = request.POST['password']

    print ("Attempting login for %s" % username)

    user = authenticate(username=username, password=password)
    if user:
        if user.is_active:
            auth.login(request, user)
            print ("Login successful")
            return HttpResponseRedirect(reverse("codeshare:index"))
        else:
            return HttpResponseRedirect("Your account is disabled!")
    else:
        return HttpResponse("Invalid login details")


def register(request):
    try:
        if User.objects.get(username=request.POST['username']):
            return HttpResponse("Username already taken")
    except:
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            instructor_form = InstructorForm(
                request.POST, instance=Instructor(user=user))
            if instructor_form.is_valid():
                instructor = instructor_form.save(commit=False)
                instructor.user = user
                instructor.save()

            print ("Registeration successful")
            auth.login(request, user)
            return HttpResponseRedirect(reverse("codeshare:index"))


def logout(request):
    print ("Signing off...")
    auth.logout(request)
    return HttpResponseRedirect(reverse("codeshare:index"))
