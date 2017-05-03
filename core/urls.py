from django.conf.urls import patterns, url
from django.conf import settings


urlpatterns = patterns(
    '',
    url(r'^$', 'core.views.home', name="home"),
    url(r'^product/([0-9]*)$', 'core.views.product', name="product"),
    url(r'^mp-notifications$', 'core.views.mp_notifications', name="mp-notifications"),
)