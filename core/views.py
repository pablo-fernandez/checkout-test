# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from core.models import Product
import mercadopago


def home(request):
    context = {
                'products': Product.objects.all(),
    }
    return render(request, 'core/home.html', context)


def product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    preference = {
        "items": [
            {
                "title": product.name,
                "quantity": 1,
                "currency_id": "ARS",
                "unit_price": float(product.price)
            }
        ]
    }

    mp = mercadopago.MP(settings.MP_CLIENT_ID, settings.MP_CLIENT_SECRET)

    preferenceResult = mp.create_preference(preference)
    
    payment_url = preferenceResult["response"]["sandbox_init_point"]

    context = {
        'payment_url': payment_url,
        'product': product,
    }
    return render(request, 'core/product.html', context)
