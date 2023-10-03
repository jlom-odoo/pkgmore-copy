from odoo import _, models


class Picking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super().button_validate()
        if self.state == 'done':
            ir_actions_report_sudo = self.env['ir.actions.report'].sudo()
            action_report_delivery = self.env.ref('stock.action_report_delivery')
            delivery_slip = action_report_delivery.sudo()
            content, _content_type = ir_actions_report_sudo._render_qweb_pdf(delivery_slip, res_ids=self.ids)
            self.env['ir.attachment'].create({
                'name': _('Delivery Slip - %s - %s' % (self.partner_id.name or '', self.name)),
                'type': 'binary',
                'mimetype': 'application/pdf',
                'raw': content,
                'res_model': self._name,
                'res_id': self.id,
                'move_origin': self.sale_id.name,
            })
        return res
