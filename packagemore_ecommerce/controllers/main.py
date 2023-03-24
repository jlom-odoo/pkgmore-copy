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
       