from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^(?P<course_name>[^/]+)/$', views.course, name='course'),
    url(r'^(?P<course_name>[^/]+)/(?P<snippet_id>[0-9]+)/delete/$', views.delete, name='delete'),
]
