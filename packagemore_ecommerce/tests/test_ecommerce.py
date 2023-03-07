from odoo.addons.base.tests.common import HttpCaseWithUserPortal
from odoo.tests import tagged
from odoo import http
from odoo.http import root
from odoo.addons.packagemore_ecommerce.controllers.main import CheckoutRestrict 
from odoo.addons.website.tools import MockRequest

@tagged('post_install', '-at_install', 'package')
class TestEcommerce(HttpCaseWithUserPortal):

    @classmethod
    def setUpClass(self):
        super(TestEcommerce, self).setUpClass() 
        self.Controller = CheckoutRestrict()
        self.website = self.env.ref('website.default_website')
        self.attrib_set = {}
        self.post = {
            'order': self.website.shop_default_sort
        }
        self.search = ''
        self.options = {
            'displayDescription': True, 
            'displayDetail': True, 
            'displayExtraDetail': True, 
            'displayExtraLink': True, 
            'displayImage': True, 
            'allowFuzzy': True, 
            'category': None, 
            'min_price': 0.0, 
            'max_price': 0.0, 
            'attrib_values': [],
            'display_currency': self.env.ref('base.main_company').currency_id
        }

        self.regular_product = self.env['product.template'].create({
            'name': 'Regular Product',
            'list_price': 100.00,
            'is_published': True
        })

        self.my_exclusive_product = self.env['product.template'].create({
            'name': 'My Exclusive Product',
            'list_price': 88.00,
            'is_published': True
        })

        self.dummy_customer = self.env['res.partner'].create({
            'name': 'Dummy Dan'
        })

        self.other_exclusive_product = self.env['product.template'].create({
            'name': 'Dan Exclusive Product',
            'list_price': 88.00,
            'is_published': True,
            'exclusive_customer': self.dummy_customer.id
        })



    def test_unregistered_user(self):
        #Non portal user should raise access error when trying to checkout
        session = self.authenticate(None, None)
        root.session_store.save(session)
        res = self.url_open(
            url = self.base_url() + '/shop/checkout',
            data= {
                'csrf_token': http.Request.csrf_token(self),
            }
        )
        self.assertEqual(res.status_code, 403) #403 is HTTP code for access error


    def test_registered_user(self):
        #Portal user should be able to checkout
        session = self.authenticate(self.user_portal.login, self.user_portal.login)
        root.session_store.save(session)
        res = self.url_open(
            url = self.base_url() + '/shop/checkout',
            data= {
                'csrf_token': http.Request.csrf_token(self),
            }
        )
        self.assertEqual(res.status_code, 200) #200 is HTTP code for OK


    def test_product_filter(self):
        self.my_exclusive_product.write({
            'exclusive_customer': self.env.user.partner_id.id
        })
        
        with MockRequest(self.env, website=self.website):
            res = self.Controller._shop_lookup_products(self.attrib_set, self.options, self.post, self.search, self.website)
            product_ids = map(lambda x: x.id, res[2])
        self.assertTrue(self.regular_product.id in product_ids)
        self.assertTrue(self.my_exclusive_product.id in product_ids)       
        self.assertFalse(self.other_exclusive_product.id in product_ids)
        
