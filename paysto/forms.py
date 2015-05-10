#-*- coding: utf-8 -*-
from django import forms


class PaymentForm(forms.Form):
    PAYSTO_SHOP_ID = forms.CharField(widget=forms.HiddenInput())
    PAYSTO_SUM = forms.DecimalField(widget=forms.HiddenInput())
    PAYSTO_INVOICE_ID = forms.CharField(widget=forms.HiddenInput())
    PAYSTO_DESC = forms.CharField(widget=forms.HiddenInput(), required=False)
    PayerEmail = forms.EmailField(widget=forms.HiddenInput(), required=False)