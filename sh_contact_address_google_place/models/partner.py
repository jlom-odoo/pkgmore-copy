# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api
import json


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sh_contact_google_location = fields.Char('Enter Location')

    sh_contact_place_text = fields.Char('Enter location', copy=False)
    sh_contact_place_text_main_string = fields.Char(
        'Enter location ', copy=False)

    @api.onchange('sh_contact_place_text_main_string')
    def onchange_technical_google_text_main_string(self):
        """to seve name in google field"""

        if self.sh_contact_place_text_main_string:
            self.sh_contact_google_location = self.sh_contact_place_text_main_string

    @api.onchange('sh_contact_place_text')
    def onchange_technical_google_text(self):
        """to place info to std. address fields"""

        if self.sh_contact_place_text:
            google_place_dict = json.loads(self.sh_contact_place_text)
            if google_place_dict and google_place_dict.get('postcode', ''):
                self.zip = google_place_dict.get('postcode', '')
            else:
                self.zip = ''

            if google_place_dict and google_place_dict.get('street', ''):
                self.street = google_place_dict.get('street', '')
            else:
                self.street = ''

            if google_place_dict and google_place_dict.get('street2', ''):
                self.street2 = google_place_dict.get('street2', '')
            else:
                self.street2 = ''

            if google_place_dict and google_place_dict.get('city', ''):
                self.city = google_place_dict.get('city', '')
            else:
                self.city = ''

            if google_place_dict and google_place_dict.get('country', False):
                self.country_id = google_place_dict.get('country', False)
            else:
                self.country_id = False

            if google_place_dict and google_place_dict.get('state', False):
                self.state_id = google_place_dict.get('state', False)
            else:
                self.state_id = False
