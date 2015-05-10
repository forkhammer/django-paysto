#-*- coding: utf-8 -*-
from django import template
from paysto import PAYSTO_ONLINE_MERCHANT_NOCART_URL
from paysto.forms import PaymentForm
from django.conf import settings
from paysto.models import BasePayment
from django.utils.safestring import mark_safe


register = template.Library()


@register.inclusion_tag('paysto/payment-form.html', takes_context=True)
def payment_form(context, payment):
    form = PaymentForm(data={
        'PAYSTO_SHOP_ID': settings.PAYSTO_SHOP_ID,
        'PAYSTO_SUM': payment.total,
        'PAYSTO_INVOICE_ID': payment.id,
        'PAYSTO_DESC': payment.description,
        'PayerEmail': payment.user.email
    })
    return {
        'form': form,
        'action': PAYSTO_ONLINE_MERCHANT_NOCART_URL
    }

@register.filter
def payment_status(status):
    if status == BasePayment.STATUS_CONFIRMED:
        return mark_safe('<span class="text-success">%s</span>' % BasePayment.STATUSES[status])
    if status == BasePayment.STATUS_WAITING:
        return mark_safe('<span class="text-muted">%s</span>' % BasePayment.STATUSES[status])
    if status == BasePayment.STATUS_ERROR:
        return mark_safe('<span class="text-danger">%s</span>' % BasePayment.STATUSES[status])
    else:
        return mark_safe(BasePayment.STATUSES[status])