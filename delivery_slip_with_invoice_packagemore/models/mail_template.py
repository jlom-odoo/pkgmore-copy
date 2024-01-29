from odoo import models


class MailTemplate(models.Model):
    _inherit = "mail.template"

    def generate_email(self, res_ids, fields):
        res = super().generate_email(res_ids, fields)
        for res_id, result_values in res.items():
            if 'attachments' in result_values:
                invoice_id = self.env['account.move'].browse(res_id)
                for ds in invoice_id.delivery_slips_attachment_ids:
                    result_values['attachments'].append(("%s.pdf" % ds.display_name, ds.datas))
        return res
