from odoo import models


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    def _get_applicable_rules(self, products, date, **kwargs):
        applicable_rules = super()._get_applicable_rules(products, date, **kwargs)
        return applicable_rules.sorted("min_quantity")
