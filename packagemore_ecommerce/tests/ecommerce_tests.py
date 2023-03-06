# from odoo.addons.base.tests.common import HttpCaseWithUserDemo
from odoo.tests import tagged, common
# from odoo.tests.common import TransactionCase
# from odoo.addons.website_sale.tests.test_sitemap import TestSitemap

@tagged('post_install', '-at_install', 'package')
class NewTestSitemap(common.TransactionCase):

    def setUp(self):
        super.setUp()

    def test_02(self):
        print("garting \n\n\n\n\n")
        self.assertEqual(0,1)


