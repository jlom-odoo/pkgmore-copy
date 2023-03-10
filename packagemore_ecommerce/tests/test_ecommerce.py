from odoo.addons.base.tests.common import HttpCaseWithUserPortal
from odoo.tests import tagged
from odoo import http
from odoo.http import root
from odoo.addons.packagemore_ecommerce.controllers.main import CheckoutRestrict 


@tagged('post_install', '-at_install')
class TestEcommerce(HttpCaseWithUserPortal):

    @classmethod
    def setUpClass(self):
        super(TestEcommerce, self).setUpClass() 
        self.Controller = CheckoutRestrict()
        self.website = self.env.ref('website.default_website')


        self.regular_product = self.env['product.template'].create({
            'name': 'Regular Product',
            'list_price': 100.00,
            'is_published': True
        })

        portal_group = self.env.ref('base.group_portal')

        [self.user, self.other_user] = self.env['res.users'].create([
            {
                'name': 'Testing Tim',
                'login': 'timlogin',
                'groups_id': [6, 0, portal_group.id]
            },
            {
                'name': 'Dummy Dan',
                'login': 'danlogin',
                'groups_id': [6, 0, portal_group.id]
            }, 
        ])

        [self.my_exclusive_product, self.other_exclusive_product] = self.env['product.template'].create([
            {
                'name': 'My Exclusive Product',
                'list_price': 88.00,
                'is_published': True,
                'exclusive_customer': self.user.id
            },
            {
                'name': 'Dan Exclusive Product',
                'list_price': 88.00,
                'is_published': True,
                'exclusive_customer': self.other_user.id
            }
        ])


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
            data = {
                'csrf_token': http.Request.csrf_token(self),
            }
        )
        self.assertEqual(res.status_code, 200) #200 is HTTP code for OK


    def test_product_filter(self):

        product_ids = [self.regular_product.id, self.my_exclusive_product.id, self.other_exclusive_product.id]


        search_results = self.env['product.template'].with_user(self.user).search([['id', 'in', product_ids]])
        

        self.assertTrue(self.regular_product in search_results)
        self.assertTrue(self.my_exclusive_product in search_results)      
        self.assertFalse(self.other_exclusive_product in search_results)
    