from odoo import models, fields, _


class ProductTemplate(models.Model):
    _inherit='product.template'

    exclusive_customer = fields.Many2one(
        comodel_name='res.partner',
        string="Exclusive customer",
        help=_("""
        When this field is not set, products are visible to all partners on ecommerce. 
        When a partner is set, product is only visible to that partner on ecommerce
        """),
    )
    