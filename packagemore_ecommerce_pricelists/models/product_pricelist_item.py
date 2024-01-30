from odoo import models


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    def _is_applicable_for(self, product, qty_in_product_uom):
        self.ensure_one()
        if qty_in_product_uom == 1.0:
            qty_in_product_uom = self.min_quantity
        return super()._is_applicable_for(product, qty_in_product_uom)
