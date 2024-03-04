# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move"

    related_picking_ids = fields.Many2many("stock.picking", )

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _create_invoices(self, grouped=False, final=False, date=None):
        move_ids = self.env["account.move"]
        for rec in self:
            old_invoice_ids = rec.invoice_ids
            old_related_picking_ids = self.env["stock.picking"]
            if old_invoice_ids:
                old_related_picking_ids = old_invoice_ids.mapped("related_picking_ids")
            moves = super(SaleOrder, rec)._create_invoices(grouped, final, date)
            move_ids += moves
            picking_ids = rec.picking_ids.filtered(lambda picking: picking.state == "done" and picking.picking_type_id.attach_picking_with_invoice and picking.id not in old_related_picking_ids.ids)
            if picking_ids:
                for move in moves:
                    move.related_picking_ids = [(6, 0, picking_ids.ids)]
        return move_ids

class OperationType(models.Model):
    _inherit = "stock.picking.type"

    attach_picking_with_invoice = fields.Boolean()
    is_dropshipping = fields.Boolean()

class AccountInvoiceSend(models.TransientModel):
    _inherit = 'account.invoice.send'

    @api.onchange('template_id')
    def onchange_template_id(self):
        super().onchange_template_id()
        rec_ids = self
        if len(rec_ids) == 1:
            if rec_ids.invoice_ids:
                attachment_ids = []
                for inv in rec_ids.invoice_ids:
                    if inv.related_picking_ids:
                        for picking_id in inv.related_picking_ids:
                            if picking_id.picking_type_id.is_dropshipping:
                                pdf = self.env['ir.actions.report'].sudo()._render_qweb_pdf('invoice_attach_delivery_proof.action_report_dropship', [picking_id.id])[0]
                                attachment_ids.append({'name': 'Delivery Slip - %s' % picking_id.name,'datas': base64.b64encode(pdf),'res_model': picking_id._name,'res_id': picking_id.id,'mimetype': 'application/pdf','type': 'binary'})
                            else:
                                pdf = self.env['ir.actions.report'].sudo()._render_qweb_pdf('stock.action_report_delivery', [picking_id.id])[0]
                                attachment_ids.append({'name': 'Delivery Slip - %s - %s' % (picking_id.partner_id.name or '', picking_id.name),'datas': base64.b64encode(pdf),'res_model': picking_id._name,'res_id': picking_id.id,'mimetype': 'application/pdf','type': 'binary',})
                if attachment_ids:
                    attachment_ids = self.env['ir.attachment'].create(attachment_ids)
                    attachment_ids = [(4, att_id.id) for att_id in attachment_ids]
                    rec_ids.attachment_ids = attachment_ids