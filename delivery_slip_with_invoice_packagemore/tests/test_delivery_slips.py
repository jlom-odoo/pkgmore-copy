import odoo.tests
import logging
from odoo.tests import Form
from odoo.fields import Command

_logger = logging.getLogger(__name__)


class TestAccountMove(odoo.tests.common.TransactionCase):

    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass()

        cls.supplier = cls.env['res.partner'].create({'name': 'Vendor'})
        cls.customer = cls.env['res.partner'].create({'name': 'Customer'})

        cls.product1 = cls.env['product.product'].create({
            'name': "Test Product 1",
        })

        cls.product2 = cls.env['product.product'].create({
            'name': "Test Product 2",
        })

        cls.dropshipping_route = cls.env.ref('stock_dropshipping.route_drop_shipping')

        cls.dropship_product = cls.env['product.product'].create({
            'name': "Test Dropship Product",
            'type': "product",
            'categ_id': cls.env.ref('product.product_category_1').id,
            'lst_price': 100.0,
            'standard_price': 0.0,
            'uom_id': cls.env.ref('uom.product_uom_unit').id,
            'uom_po_id': cls.env.ref('uom.product_uom_unit').id,
            'seller_ids': [(0, 0, {
                'delay': 1,
                'partner_id': cls.supplier.id,
                'min_qty': 1.0
            })],
        })

        cls.lot_dropship_product = cls.env['product.product'].create({
            'name': "Serial product",
            'tracking': 'lot',
            'seller_ids': [(0, 0, {'partner_id': cls.supplier.id})],
            'route_ids': [(4, cls.dropshipping_route.id, 0)]
        })

        cls.sale_order0 = cls.env['sale.order'].create({
            'partner_id': cls.customer.id,
            'order_line': [
                Command.create({
                    'product_id': cls.product1.id,
                    'product_uom_qty': 1,
                    'price_unit': 5,
                })
            ],
        })

        cls.sale_order1 = cls.sale_order0.copy()

        cls.sale_order2 = cls.env['sale.order'].create({
            'partner_id': cls.customer.id,
            'order_line': [
                Command.create({
                    'product_id': cls.product1.id,
                    'product_uom_qty': 1,
                    'price_unit': 5,
                }),
                Command.create({
                    'product_id': cls.product2.id,
                    'product_uom_qty': 1,
                    'price_unit': 1,
                })
            ],
        })

    def test_delivery_slips_attachment_ids(self):
        # Verify the number of delivery slips attached to a SO:
        _logger.warning('Test the number of delivery slips attached to the invoice')

        # No delivery:
        self.sale_order0.action_confirm()
        self.sale_order0._create_invoices()
        invoice0 = self.sale_order0.invoice_ids
        invoice0.action_post()
        invoice0.action_invoice_sent()
        self.assertEqual(len(invoice0.delivery_slips_attachment_ids),
                         0,
                         "The number of delivery slips is incorrect. Expected: 0.")

        # One delivery slip:
        self.sale_order1.action_confirm()
        self.sale_order1.picking_ids.move_ids[0].quantity_done = 1
        self.sale_order1.picking_ids.button_validate()
        self.sale_order1._create_invoices()
        invoice1 = self.sale_order1.invoice_ids
        invoice1.action_post()
        invoice1.action_invoice_sent()
        self.assertEqual(len(invoice1.delivery_slips_attachment_ids),
                         1,
                         "The number of delivery slips is incorrect. Expected: 1.")

        # Two delivery slips (with backorder):
        self.sale_order2.action_confirm()
        self.sale_order2.picking_ids.move_ids[0].quantity_done = 1
        backorder_wizard_dict = self.sale_order2.picking_ids.button_validate()
        backorder_wizard = Form(
            self.env[backorder_wizard_dict['res_model']].with_context(backorder_wizard_dict['context'])).save()
        backorder_wizard.process()
        bo = self.sale_order2.picking_ids.backorder_ids[0]
        bo.move_ids[0].quantity_done = 1.0
        bo.button_validate()
        self.sale_order2._create_invoices()
        invoice2 = self.sale_order2.invoice_ids
        invoice2.action_post()
        invoice2.action_invoice_sent()
        self.assertEqual(len(invoice2.delivery_slips_attachment_ids),
                         2,
                         "The number of delivery slips is incorrect. Expected: 2.")

        # One delivery slip (dropship):
        mto_route = self.env.ref('stock.route_warehouse0_mto')
        self.dropship_product.write({'route_ids': [(6, 0, [self.dropshipping_route.id, mto_route.id])]})
        sale_order = self.env['sale.order'].create({
            'partner_id': self.customer.id,
            'partner_invoice_id': self.customer.id,
            'partner_shipping_id': self.customer.id,
            'order_line': [(0, 0, {
                'name': self.dropship_product.name,
                'product_id': self.dropship_product.id,
                'product_uom_qty': 1.00,
                'product_uom': self.dropship_product.uom_id.id,
                'price_unit': 12,
            })],
            'pricelist_id': self.env.ref('product.list0').id,
            'picking_policy': 'direct',
        })
        sale_order.action_confirm()
        purchase_order = self.env['purchase.order'].search([('group_id', '=', sale_order.procurement_group_id.id)])
        purchase_order.button_confirm()
        sale_order.picking_ids.move_ids[0].quantity_done = 1
        sale_order.picking_ids.button_validate()
        sale_order._create_invoices()
        invoice = sale_order.invoice_ids
        invoice.action_post()
        invoice.action_invoice_sent()
        self.assertEqual(len(invoice.delivery_slips_attachment_ids),
                         1,
                         "The number of delivery slips is incorrect. Expected: 1.")
