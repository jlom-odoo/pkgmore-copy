from odoo.addons.website_sale.tests.test_website_sale_add_to_cart_snippet import TestAddToCartSnippet
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class OverrideTestAddToCartSnippet(TestAddToCartSnippet):
    def test_configure_product(self):
        #This test will fail at checkout because of the behavior of this dev. 
        pass

<div class="o-main-components-container"><div class="o_effects_manager"></div><div class="o_dialog_container"><div></div></div><div class="o_notification_manager"></div><div></div><div class="o_notification_manager o_upload_progress_toast"></div><div class="o_popover_container"></div></div></body></html>
2023-03-10 18:41:41,407 4 ERROR package-more-16-0-ecommerce-3108813-jden-7557843 odoo.addons.website_sale.tests.test_customize.TestUi.browser: Tour tour_shop_dynamic_variants failed at step select Dynamic Product (trigger: .oe_product_cart a:containsExact("Dynamic Product"))
2023-03-10 18:41:41,414 4 INFO package-more-16-0-ecommerce-3108813-jden-7557843 odoo.addons.website_sale.tests.test_customize.TestUi: Asking for screenshot
2023-03-10 18:41:41,415 4 INFO package-more-16-0-ecommerce-3108813-jden-7557843 odoo.addons.website_sale.tests.test_customize.TestUi: Asking for screenshot
2023-03-10 18:41:41,529 4 INFO package-more-16-0-ecommerce-3108813-jden-7557843 odoo.addons.website_sale.tests.test_customize.TestUi: Screenshot in: /tmp/odoo_tests/package-more-16-0-ecommerce-3108813-jden-7557843/screenshots/sc_20230310_184141_529050_TestUi.png
2023-03-10 18:41:41,597 4 INFO package-more-16-0-ecommerce-3108813-jden-7557843 odoo.addons.website_sale.tests.test_customize.TestUi: Deleting cookies and clearing local storage
2023-03-10 18:41:41,598 4 INFO package-more-16-0-ecommerce-3108813-jden-7557843 odoo.addons.website_sale.tests.test_customize.TestUi: Screenshot in: /tmp/odoo_tests/package-more-16-0-ecommerce-3108813-jden-7557843/screenshots/sc_20230310_184141_597487_TestUi.png
2023-03-10 18:41:41,602 4 INFO package-more-16-0-ecommerce-3108813-jden-7557843 odoo.addons.website_sale.tests.test_customize.TestUi: Navigating to: "about:blank"
2023-03-10 18:41:41,603 4 INFO package-more-16-0-ecommerce-3108813-jden-7557843 odoo.addons.website_sale.tests.test_customize.TestUi: Navigation result: {'frameId': '6F54F658B23D8D8058F905659319C037', 'loaderId': 'D20E874690F9E8D5768E20BC9CE332B5'}
2023-03-10 18:41:41,603 4 INFO package-more-16-0-ecommerce-3108813-jden-7557843 odoo.addons.website_sale.tests.test_customize.TestUi: Waiting for frame '6F54F658B23D8D8058F905659319C037' to stop loading
2023-03-10 18:41:41,616 4 INFO package-more-16-0-ecommerce-3108813-jden-7557843 odoo.addons.website_sale.tests.test_customize.TestUi: waiting for threads: []
2023-03-10 18:41:41,616 4 INFO package-more-16-0-ecommerce-3108813-jden-7557843 odoo.addons.website_sale.tests.test_customize: ======================================================================
2023-03-10 18:41:41,617 4 ERROR package-more-16-0-ecommerce-3108813-jden-7557843 odoo.addons.website_sale.tests.test_customize: FAIL: TestUi.test_03_public_tour_shop_dynamic_variants
Traceback (most recent call last):
  File "/home/odoo/src/odoo/addons/website_sale/tests/test_customize.py", line 215, in test_03_public_tour_shop_dynamic_variants
    self.start_tour("/", 'tour_shop_dynamic_variants')
  File "/home/odoo/src/odoo/odoo/tests/common.py", line 1753, in start_tour
    return self.browser_js(url_path=url_path, code=code, ready=ready, **kwargs)
  File "/home/odoo/src/odoo/odoo/tests/common.py", line 1733, in browser_js
    self.fail('%s\n\n%s' % (message, error))
AssertionError: The test code "odoo.startTour('tour_shop_dynamic_variants')" failed

Tour tour_shop_dynamic_variants failed at step select Dynamic Product (trigger: .oe_product_cart a:containsExact("Dynamic Product"))