#-*- coding: utf-8 -*-
from django.conf import settings

shop_id = getattr(settings, 'PAYSTO_SHOP_ID', None)
if not shop_id:
    raise Exception(u'Не установлен PAYSTO_SHOP_ID')

payment_class = getattr(settings, 'PAYSTO_PAYMENT_CLASS', None)
if not payment_class:
    raise Exception(u'Не установлен PAYSTO_PAYMENT_CLASS')

