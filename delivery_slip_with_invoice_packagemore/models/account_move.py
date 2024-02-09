from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    delivery_slips_attachment_ids = fields.Many2many('ir.attachment')

    def action_invoice_sent(self):
        self.ensure_one()
        self.delivery_slips_attachment_ids = self.env['ir.attachment'].search([('move_origin', '=', self.invoice_origin)])
        report_action = super().action_invoice_sent()
        return report_action
