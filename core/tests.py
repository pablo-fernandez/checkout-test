# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Order, Product, InvalidStateException
from django.core.urlresolvers import reverse


class OrderTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username='test-user')
        self.product = Product.objects.create(name='Test Product', price=10.00)

    def test_complete_pending_order(self):
        order = Order.objects.create(user=self.user, product=self.product)
        self.assertEquals(order.status, 'pending')
        order.complete()
        self.assertEquals(order.status, 'complete')

    def test_cancel_pending_order(self):
        order = Order.objects.create(user=self.user, product=self.product)
        self.assertEquals(order.status, 'pending')
        order.cancel()
        self.assertEquals(order.status, 'cancel')

    def test_cancel_completed_order_must_fail(self):
        order = Order.objects.create(user=self.user, product=self.product, status='complete')
        self.assertRaises(InvalidStateException, order.cancel)

    def test_complete_canceled_order_must_fail(self):
        order = Order.objects.create(user=self.user, product=self.product, status='cancel')
        self.assertRaises(InvalidStateException, order.complete)


class UrlsTestCase(TestCase):

    def test_home_url(self):
        url = reverse('home')
        self.assertEquals(url, '/')

    def test_login_url(self):
        url = reverse('login')
        self.assertEquals(url, '/ingresar/')

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEquals(url, '/salir/')

    def test_orders_url(self):
        url = reverse('orders')
        self.assertEquals(url, '/ordenes/')

    def test_purchase_success_url(self):
        url = reverse('mp-back-success')
        self.assertEquals(url, '/compra-exitosa/')

    def test_purchase_failure_url(self):
        url = reverse('mp-back-failure')
        self.assertEquals(url, '/compra-fallida/')

    def test_purchase_pending_url(self):
        url = reverse('mp-back-pending')
        self.assertEquals(url, '/compra-pago-pendiente/')

    def test_mp_notifications_url(self):
        url = reverse('mp-notifications')
        self.assertEquals(url, '/mp-notifications/')
