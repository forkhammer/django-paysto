#-*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

PAYSTO_ONLINE_MERCHANT_NOCART_URL = 'https://paysto.com/ru/pay'

PAYSTO_IPS = [
    '66.226.72.66',
    '66.226.74.225',
    '66.226.74.226',
    '66.226.74.227',
    '66.226.74.228',
    '23.102.21.72',
    '23.102.17.162',
    '137.135.207.41',
]


def get_payment_model():
    """
    Returns the User model that is active in this project.
    """
    from django.db.models import get_model

    try:
        app_label, model_name = settings.PAYSTO_PAYMENT_MODEL.split('.')
    except ValueError:
        raise ImproperlyConfigured("PAYSTO_PAYMENT_MODEL must be of the form 'app_label.model_name'")
    payment_model = get_model(app_label, model_name)
    if payment_model is None:
        raise ImproperlyConfigured("PAYSTO_PAYMENT_MODEL refers to model '%s' that has not been installed" % settings.PAYSTO_PAYMENT_MODEL)
    return payment_model