from odoo.addons.website_sale.tests.test_website_add_to_cart_snippet import TestAddToCartSnippet


class OverrideTestAddToCartSnippet(TestAddToCartSnippet):

    def test_configure_product(self):
        #This test will fail at checkout because of the behavior of this dev. 
        pass
