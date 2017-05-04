# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
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


def login(request):
    return render(request, 'core/login.html', {})


def logout(request):
    return render(request, 'core/home.html', context)


def orders(request):
    context = {
        'orders': Order.objects.filter(user=request.user),
    }
    return render(request, 'core/orders.html', context)


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
    order = Order.objects.create(product=product, user=request.user, preference=preferenceResult["response"]["id"])

    payment_url = preferenceResult["response"]["sandbox_init_point"]

    context = {
        'payment_url': payment_url,
        'product': product,
    }
    return render(request, 'core/product.html', context)


def mp_notifications(request, **kwargs):
    # TODO: Encolar el pedido y retornar un 200 directo
    topic = request.GET['topic']
    mp_id = request.GET['id']
    process_notification.delay(topic, mp_id)
    return JsonResponse({})
