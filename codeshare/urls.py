from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<course_name>\w+)/$', views.course, name='course'),
    url(r'^(?P<course_name>\w+)/(?P<snippet_id>[0-9]+)/delete/$', views.delete, name='delete'),
]
