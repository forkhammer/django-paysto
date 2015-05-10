#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from paysto.views import *

urlpatterns = patterns('',
                        url(r'^check$', PaymentCheckView.as_view(), name='paysto_check'),
                        url(r'^result$', PaymentResultView.as_view(), name='paysto_result'),
                        url(r'^success$', PaymentSuccessView.as_view(), name='paysto_success'),
                        url(r'^fail$', PaymentSuccessView.as_view(), name='paysto_fail'),
                       )