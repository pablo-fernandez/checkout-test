# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from core.models import Product, Order
from django.http import JsonResponse
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
    order = Order.objects.create(product=product, user=request.user, preference=preferenceResult["response"]["id"])

    payment_url = preferenceResult["response"]["sandbox_init_point"]

    context = {
        'payment_url': payment_url,
        'product': product,
    }
    return render(request, 'core/product.html', context)


def mp_notifications(request, **kwargs):
    mp = mercadopago.MP(settings.MP_CLIENT_ID, settings.MP_CLIENT_SECRET)
    
    topic = request.GET['topic']
    mp_id = request.GET['id']

    merchant_order_info = None

    if topic == "payment":
        payment_info = mp.get("/collections/notifications/"+ mp_id)
        if not payment_info["status"] == 200:
            return JsonResponse({'status': payment_info["status"]})
        merchant_order_info = mp.get("/merchant_orders/" + payment_info["response"]["collection"]["merchant_order_id"])
    elif topic == "merchant_order":
        merchant_order_info = mp.get("/merchant_orders/" + mp_id)

    if merchant_order_info == None:
        raise ValueError("Error obtaining the merchant_order")

    if merchant_order_info["status"] == 200:
        return JsonResponse({
            "payment": merchant_order_info["response"]["payments"],
            "shipment": merchant_order_info["response"]["shipments"]
        })
