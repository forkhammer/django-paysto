#-*- coding: utf-8 -*-
from django.views.generic import View, TemplateView
from paysto.models import BasePayment
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from paysto import PAYSTO_IPS, get_payment_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging
import traceback


logger = logging.getLogger('paysto')


class PaymentCheckView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentCheckView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logger.info('==============================')
        logger.info('Запрос на подтверждение платежа')
        logger.info(request.POST.get('PAYSTO_INVOICE_ID'))

        result = HttpResponse()
        try:
            if not request.META['REMOTE_ADDR'] in PAYSTO_IPS:
                logger.info('Неправильный IP платежной системы')
                raise Exception(u'Неправильный IP платежной системы')

            payment_list = get_payment_model().objects.filter(id=request.POST.get('PAYSTO_INVOICE_ID'))
            if not payment_list:
                logger.info('Не найден указанный платеж')
                raise Exception(u'Не найден указанный платеж')

            payment = payment_list[0]

            if payment.total != float(request.POST.get('PAYSTO_SUM')):
                logger.info('Не сходиться сумма платежа')
                raise Exception(u'Не сходиться сумма платежа')

            if str(settings.PAYSTO_SHOP_ID) != request.POST.get('PAYSTO_SHOP_ID'):
                logger.info('Неправильный идентификатор магазина')
                raise Exception(u'Неправильный идентификатор магазина')

            if payment.status != BasePayment.STATUS_WAITING:
                logger.info('Статус платежа не подтвержден')
                raise Exception(u'Статус платежа не подтвержден')

            payment.hash_md5 = request.POST.get('PAYSTO_MD5')
            payment.transaction_id = request.POST.get('PAYSTO_PAYMENT_ID')
            payment.save()

            result.write(payment.id)
            logger.info(payment.id)

        except Exception, err:
            logger.info( traceback.format_exc())
        return result


class PaymentResultView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentResultView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logger.info('==============================')
        logger.info('Запрос на результат платежа')
        logger.info(request.POST.get('PAYSTO_INVOICE_ID'))
        result = HttpResponse()
        try:
            if not request.META['REMOTE_ADDR'] in PAYSTO_IPS:
                logger.info('Неправильный IP платежной системы')
                raise Exception(u'Неправильный IP платежной системы')

            payment_list = get_payment_model().objects.filter(id=request.POST.get('PAYSTO_INVOICE_ID'))
            if not payment_list:
                logger.info('Не найден указанный платеж')
                raise Exception(u'Не найден указанный платеж')

            payment = payment_list[0]
            if str(settings.PAYSTO_SHOP_ID) != request.POST.get('PAYSTO_SHOP_ID'):
                logger.info('Неправильный идентификатор магазина')
                raise Exception(u'Неправильный идентификатор магазина')

            if payment.transaction_id != request.POST.get('PAYSTO_PAYMENT_ID'):
                logger.info('Не совпадает номер транзакции')
                raise Exception(u'Не совпадает номер транзакции')

            payment.request_mode = request.POST.get('PAYSTO_REQUEST_MODE')
            if payment.request_mode == BasePayment.RES_CANCEL:
                payment.status = BasePayment.STATUS_REJECTED
            elif payment.request_mode == BasePayment.RES_ERROR:
                payment.status = BasePayment.STATUS_ERROR
            elif payment.request_mode == BasePayment.RES_HOLD:
                payment.request_mode = BasePayment.STATUS_ERROR
            elif payment.request_mode == BasePayment.RES_PAID:
                payment.status = BasePayment.STATUS_CONFIRMED
            payment.save()

            payment.result()

            result.write(payment.id)

        except Exception, err:
            logger.info( traceback.format_exc())
        return result


class PaymentSuccessView(TemplateView):
    template_name = 'paysto/success.html'
    payment = None

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentSuccessView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logger.info('==============================')
        logger.info('Запрос на успешность платежа')
        logger.info(request.POST.get('PAYSTO_INVOICE_ID'))

        payment_list = get_payment_model().objects.filter(id=request.POST.get('PAYSTO_INVOICE_ID'))
        if not payment_list:
            logger.info('Не найден указанный платеж')
            raise Exception('Не найден указанный платеж')

        self.payment = payment_list[0]
        if str(settings.PAYSTO_SHOP_ID) != request.POST.get('PAYSTO_SHOP_ID'):
            logger.info('Неправильный идентификатор магазина')
            raise Exception('Неправильный идентификатор магазина')

        if self.payment.transaction_id != request.POST.get('PAYSTO_PAYMENT_ID'):
            logger.info('Не совпадает номер транзакции')
            raise Exception('Не совпадает номер транзакции')

        return super(PaymentSuccessView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PaymentSuccessView, self).get_context_data(**kwargs)
        if self.payment:
            context['title'] = BasePayment.STATUSES[self.payment.status]
            context['payment'] = self.payment
        else:
            context['title'] = 'Платеж не найден'
        return context
