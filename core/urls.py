from django.conf.urls import patterns, url
from django.conf import settings


urlpatterns = patterns(
    '',
    url(r'^$', 'core.views.home', name="home"),
)