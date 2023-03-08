from odoo import http, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.exceptions import AccessError


class CheckoutRestrict(WebsiteSale):

    @http.route(['/shop/checkout'], type='http', auth="public", website=True, sitemap=False)
    def checkout(self, **post):
        user = request.env.user
        if not user.has_group('base.group_portal'):
            raise AccessError(_('You need to be logged into your portal account, please sign in with your portal account to be able to complete your order in the cart'))
        else:
            return super(CheckoutRestrict, self).checkout(**post)
        
    def _shop_lookup_products(self, attrib_set, options, post, search, website):
        fuzzy_search_term, product_count, search_product = super(CheckoutRestrict, self)._shop_lookup_products(attrib_set, options, post, search, website)
        partner_id = request.env.user.partner_id.id
        search_product = search_product.filtered(lambda product: not product.exclusive_customer or product.exclusive_customer.id == partner_id)
        product_count = len(search_product)
        return fuzzy_search_term, product_count, search_product
       