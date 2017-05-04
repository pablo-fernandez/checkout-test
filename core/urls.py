from django.conf.urls import patterns, url
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = patterns(
    '',
    url(r'^$', 'core.views.home', name="home"),
    url(r'^ingresar/$', auth_views.login, {'template_name': 'core/login.html'}, name='login'),
    url(r'^salir/$', auth_views.logout, {'template_name': 'core/logout.html'}, name='logout'),
    url(r'^ordenes$', 'core.views.orders', name="orders"),
    url(r'^producto/([0-9]*)$', 'core.views.product', name="product"),
    url(r'^comprar/([0-9]*)$', 'core.views.purchase', name="purchase"),
    url(r'^mp-notifications$', 'core.views.mp_notifications', name="mp-notifications"),
)