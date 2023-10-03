from odoo import fields, models


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    move_origin = fields.Char()
