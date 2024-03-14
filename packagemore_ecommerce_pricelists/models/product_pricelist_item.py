from odoo import models


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    def _is_applicable_for(self, product, qty_in_product_uom):
        self.ensure_one()
        if qty_in_product_uom == 1.0 and product:
            prod_tmpl = product
            if product._name == "product.product":
                prod_tmpl = product.product_tmpl_id
            qty_in_product_uom = min(
                (x.min_quantity for x in self.pricelist_id.item_ids if x.product_tmpl_id == prod_tmpl), 
                default=1.0)
        return super()._is_applicable_for(product, qty_in_product_uom)
