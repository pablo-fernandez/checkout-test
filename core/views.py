# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from core.models import Product, Order
from django.http import JsonResponse
from core.tasks import process_notification
import mercadopago


def home(request):
    context = {
                'products': Product.objects.all(),
    }
    return render(request, 'core/home.html', context)


def orders(request):
    context = {
        'orders': Order.objects.filter(user=request.user),
    }
    return render(request, 'core/orders.html', context)


def product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    context = {
        'product': product,
    }
    return render(request, 'core/product.html', context)


def purchase(request, product_id):
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
    order = Order.objects.create(product=product, user=request.user, preference=preferenceResult["response"]["id"])

    payment_url = preferenceResult["response"]["sandbox_init_point"]

    return redirect(payment_url)


def mp_notifications(request, **kwargs):
    topic = request.GET['topic']
    mp_id = request.GET['id']
    process_notification.delay(topic, mp_id)
    return JsonResponse({})
