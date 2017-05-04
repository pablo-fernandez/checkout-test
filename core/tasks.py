# -*- coding: utf-8 -*-
# celery -A checkout worker -l info
import json
from celery import Celery

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
        # TODO: ACTUALIZAR BD
        # "payment": merchant_order_info["response"]["payments"],
        # "shipment": merchant_order_info["response"]["shipments"]
