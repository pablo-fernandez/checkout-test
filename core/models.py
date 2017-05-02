# -*- coding: utf-8 -*-
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name=u'Nombre', unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default='0.00')


    class Meta:
        verbose_name = u'Producto'
        verbose_name_plural = u'Productos'

    def __unicode__(self):
        return u"{} - ${}".format(self.name, self.price)
