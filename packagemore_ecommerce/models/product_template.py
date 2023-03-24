from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit='product.template'

    exclusive_partner = fields.Many2one(
        comodel_name='res.partner',
        string='Exclusive partner',
        help="""When this field is not set, products are visible to all partners on ecommerce. 
        When a company is set, product is only visible to that partners within that company""",
    )
    