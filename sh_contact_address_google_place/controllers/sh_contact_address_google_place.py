# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import http
from odoo.http import request


class CustomController(http.Controller):

    # custom controller to get api key from res config
    @http.route('/sh_get_google_api_key', type='json', auth="public")
    def sh_get_google_api_key(self):
        company_id = request.env.user.company_id
        if company_id and company_id.sh_is_enable_google_api_key and company_id.sh_google_api_key:
            return {'api_key': company_id.sh_google_api_key}
        return False

    # custom controller to get country and state id from names
    @http.route(['/sh_get_country_state_code'], type='json', auth="public", website=True)
    def sh_get_country_state_code(self, country_name='', state_name='', **post):
        country_name = country_name or ''
        state_name = state_name or ''
        code = ''

        country_code = request.env["res.country"].sudo().search(
            [('name', '=', country_name)], limit=1)
        if country_code:
            code = country_code.id if country_code else ''
            country_name = country_code.name if country_code else ''

        state_code = request.env["res.country.state"].sudo().search(
            [('name', '=', state_name)], limit=1)
        if state_code:
            state_name = state_code.name if state_code else ''
            state_code = state_code.id if state_code else ''
        return {
            'country_code': code or False,
            'country_name': country_name or '',
            'state_code': state_code or False,
            'state_name': state_name or ''
        }
