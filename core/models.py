# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class InvalidStateException(Exception):
    pass

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name=u'Nombre', unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')


    class Meta:
        verbose_name = u'Producto'
        verbose_name_plural = u'Productos'

    def __unicode__(self):
        return u"{} - ${}".format(self.name, self.price)


class Order(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    status = models.CharField(max_length=10, default='pending')
    preference = models.CharField(max_length=50)
    mporder = models.CharField(max_length=50, null=True, blank=True)    

    def complete():
        if not self.status == 'pending':
            raise InvalidStateException
        self.status = 'complete'
        self.save()

    def cancel():
        if not self.status == 'pending':
            raise InvalidStateException
        self.status = 'cancel'
        self.save()
