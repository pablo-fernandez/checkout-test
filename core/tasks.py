# -*- coding: utf-8 -*-
# celery -A checkout worker -l info
import json
from celery import Celery
from core.models import Order


app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task()
def process_notification(topic, mp_id):
    mp = mercadopago.MP(settings.MP_CLIENT_ID, settings.MP_CLIENT_SECRET)
    merchant_order_info = None

    if topic == "payment":
        payment_info = mp.get("/collections/notifications/"+ mp_id)
        if not payment_info["status"] == 200:
            raise ValueError("Error obtaining payment info")
        merchant_order_info = mp.get("/merchant_orders/" + payment_info["response"]["collection"]["merchant_order_id"])
    elif topic == "merchant_order":
        merchant_order_info = mp.get("/merchant_orders/" + mp_id)

    if merchant_order_info == None:
        raise ValueError("Error obtaining the merchant_order")

    if merchant_order_info["status"] == 200:
        preference = merchant_order_info["response"]["preference_id"]
        mporder_id = merchant_order_info["response"]["id"]

        order = None

        try:
            order = Order.objects.get(mporder=mporder_id)
        except Order.DoesNotExist:
            try:
                order = Order.objects.get(preference=preference)
            except Order.DoesNotExist:
                raise ValueError("Order not found")

        if not order.mporder:
            order.mporder = mporder_id
            order.save()

        mp_status = merchant_order_info["response"]["status"]
        if mp_status  == "closed" and order.status == 'pending':
            order.complete()
        elif mp_status == "expired" and order.status == 'pending':
            order.cancel()
        order.mporder = merchant_order_info["response"]["id"]
