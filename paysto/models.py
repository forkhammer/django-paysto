#-*- coding: utf-8 -*-
from django.db import models
import random
import uuid


class BasePayment(models.Model):

    STATUS_WAITING = 'w'    #ожидает оплаты
    STATUS_CONFIRMED = 'c'  #платеж успешно завершен
    STATUS_REJECTED = 'r'   #платеж отменен
    STATUS_ERROR = 'e'      #платеж завершен с ошибкой
    STATUS_INPUT = 'i'      #хз чо за херня

    STATUSES = {
        STATUS_WAITING: 'Ожидает оплаты',
        STATUS_CONFIRMED: 'Платеж завершен',
        STATUS_REJECTED: 'Платеж отменен',
        STATUS_ERROR: 'Ошибка платежа',
        STATUS_INPUT: 'Input'
    }

    RES_BILLED = 'RES_BILLED'   #заявка отправлена на оплату
    RES_CANCEL = 'RES_CANCEL'   #покупатель отказался от покупки
    RES_CREATED = 'RES_CREATED' #заявка зарегистрирована
    RES_ERROR = 'RES_ERROR'     #при платеже произошли ошибки
    RES_HOLD = 'RES_HOLD'       #заявка приостановлена
    RES_PAID = 'RES_PAID'       #оплата состоялась
    REQUEST_MODES = {
        RES_BILLED: 'заявка отправлена на оплату',
        RES_CANCEL: 'покупатель отказался от покупки',
        RES_CREATED: 'заявка зарегистрирована',
        RES_ERROR: 'при платеже произошли ошибки',
        RES_HOLD: 'заявка приостановлена',
        RES_PAID: 'оплата состоялась'
    }

    status = models.CharField(max_length=1, choices=STATUSES.items(),
                              default=STATUS_WAITING)
    #: Creation date and time
    created = models.DateTimeField(auto_now_add=True)
    #: Date and time of last modification
    modified = models.DateTimeField(auto_now=True)
    #: Transaction ID (if applicable)
    transaction_id = models.CharField(max_length=255, blank=True)
    #: Currency code (may be provider-specific)
    currency = models.CharField(max_length=10, default='RUB')
    #: Total amount (gross)
    total = models.DecimalField(max_digits=9, decimal_places=2, default='0.0')
    delivery = models.DecimalField(max_digits=9, decimal_places=2,
                                   default='0.0')
    tax = models.DecimalField(max_digits=9, decimal_places=2, default='0.0')
    description = models.TextField(blank=True, default='')
    extra_data = models.TextField(blank=True, default='')
    token = models.CharField(max_length=36, blank=True, default='')
    hash_md5 = models.CharField(max_length=50, blank=True, null=True, default='')
    request_mode = models.CharField(max_length=20, blank=True, null=True, choices=REQUEST_MODES.items())

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.id

    def change_status(self, status):
        '''
        Updates the Payment status and sends the status_changed signal.
        '''
        from paysto.signals import paysto_status_changed
        self.status = status
        self.save()
        paysto_status_changed.send(sender=type(self), instance=self)

    def result(self):
        if self.status == self.STATUS_CONFIRMED:
            self.success()
        elif self.status in [self.STATUS_ERROR, self.STATUS_REJECTED]:
            self.fail()

    def success(self):
        pass

    def fail(self):
        pass