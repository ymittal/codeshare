from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^(?P<course_name>[^/]+)/$', views.course, name='course'),
    url(r'^(?P<course_name>[^/]+)/(?P<snippet_id>[0-9]+)/delete/$',
        views.delete, name='delete'),
]
