# from odoo.addons.base.tests.common import HttpCaseWithUserDemo
from odoo.tests import tagged, common
# from odoo.tests.common import TransactionCase
import json


@tagged('package', 'post_install', '-at_install')
class TestEcommerce(common.TransactionCase):

    def test_non_portal_user_checkout(self):
        print(self.base_url())
        self.assertEqual(0, 1)

    def test_portal_user_checkout(self):
        self.assertEqual(0, 1)

    def test_view_exclusive_product(self):
        self.assertEqual(0, 1)

    def test_restrict_view_exclusive_product(self):
        self.assertEqual(0, 1)