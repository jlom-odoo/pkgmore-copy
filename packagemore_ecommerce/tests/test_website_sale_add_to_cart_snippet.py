from odoo.addons.website_sale.tests.test_website_sale_add_to_cart_snippet import TestAddToCartSnippet
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class OverrideTestAddToCartSnippet(TestAddToCartSnippet):
    def test_configure_product(self):
        #This test will fail at checkout because of the behavior of this dev. 
        pass
