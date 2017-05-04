# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Order, Product, InvalidStateException


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
