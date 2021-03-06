# coding=utf-8
from django.conf import settings
from django.utils.http import urlquote_plus

from apps.order.tests import DBTestBase
from apps.order.models import Order
from apps.order.exceptions import OrderException
from apps.payment.exceptions import  PaymentException



site_host = getattr(settings, 'SITE_HOST', None)
class OrderPaymentTest(DBTestBase):

    def setUp(self):
        super(OrderPaymentTest, self).setUp()
        self.sku1 = self.entity.add_sku({
            'color': 'red',
            'size':165
        })
        self.sku1.stock = 5
        self.sku1.origin_price = 0.02
        self.sku1.promo_price = 0.01
        self.sku1.save()

        self.sku2 = self.entity.add_sku({
            'color':'black',
            'size': 128
        })
        self.sku2.stock = 5
        self.sku2.origin_price = 0.03
        self.sku2.promo_price = 0.01
        self.sku2.save()

        self.the_user.add_sku_to_cart(self.sku1)
        self.the_user.add_sku_to_cart(self.sku2)

        self.order = self.the_user.checkout()

    def test_order_status(self):
        pass

    def test_tb_payment_url_generate(self):
        url = self.order.generate_alipay_payment_url()
        print(url)

        self.assertEqual('https://mapi.alipay.com/gateway.do?' in url , True)
        self.assertIn(urlquote_plus(site_host),url)

    def test_tb_payment_notify_url_host(self):
        url = self.order.generate_alipay_payment_url()
        print(url)
        self.assertEqual('https://mapi.alipay.com/gateway.do?' in url , True)
        self.assertIn(urlquote_plus(site_host), url )


