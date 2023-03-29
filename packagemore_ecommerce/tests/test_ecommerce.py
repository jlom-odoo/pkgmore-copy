from odoo.addons.base.tests.common import HttpCaseWithUserPortal
from odoo.tests import tagged
from odoo import http
from odoo.http import root
from odoo.addons.packagemore_ecommerce.controllers.main import CheckoutRestrict 
from odoo.tools import mute_logger


@tagged('post_install', '-at_install')
class TestEcommerce(HttpCaseWithUserPortal):

    @classmethod
    def setUpClass(self):
        super(TestEcommerce, self).setUpClass() 
        self.Controller = CheckoutRestrict()
        self.website = self.env.ref('website.default_website')

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

        [self.my_company, self.other_company] = self.env['res.partner'].create([
            {
                'name': 'My Company',
                'is_company': True
            }, 
            {
                'name': 'Other Company',
                'is_company': True
            }
        ])

        self.user.partner_id.write({
            'parent_id': self.my_company.id
        })

        [
            self.regular_product,
            self.my_product, 
            self.other_partner_product,
            self.my_company_product,
            self.other_company_product
        ] = self.env['product.template'].create([
            {
                'name': 'Regular Product',
                'list_price': 88.00,
                'is_published': True
            },
            {
                'name': 'my product',
                'list_price': 88.00,
                'is_published': True,
                'exclusive_partner': self.user.partner_id.id
            },
            {
                'name': 'other partner product',
                'list_price': 88.00,
                'is_published': True,
                'exclusive_partner': self.other_user.partner_id.id
            },
            {
                'name': 'my company product',
                'list_price': 88.00,
                'is_published': True,
                'exclusive_partner': self.my_company.id
            },
            {
                'name': 'other company product',
                'list_price': 88.00,
                'is_published': True,
                'exclusive_partner': self.other_company.id
            }
        ])


    def test_unregistered_user(self):
        #Non portal user should raise access error when trying to checkout
        session = self.authenticate(None, None)
        root.session_store.save(session)

        with mute_logger('odoo.http'): #mute 403 warning
            res = self.url_open(
                url = self.base_url() + '/shop/checkout',
                data= {
                    'csrf_token': http.Request.csrf_token(self),
                }
            )
            self.assertEqual(res.status_code, 403, 'Non-portal user should not be able to reach checkout') #403 is HTTP code for access error


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

        self.assertEqual(res.status_code, 200, 'Portal user should able to reach checkout') #200 is HTTP code for OK



    def test_view_my_product(self):

        search_results = self.env['product.template'].with_user(self.user).search([])

        self.assertTrue(self.regular_product in search_results, 'User should be able to view regular products')

        self.assertTrue(self.my_product in search_results, 'User should be able to view product exclusive to them') 

        self.assertTrue(self.my_company_product in search_results, 'User should be able to view product exclusive to their company')

        self.assertFalse(self.other_company_product in search_results, 'User should not be able to view product exclusive to another company')

        self.assertFalse(self.other_partner_product in search_results, 'User should not be able to view product exclusive to another partner, even within the same company')

    