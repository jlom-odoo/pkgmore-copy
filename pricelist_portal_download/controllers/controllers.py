# -*- coding: utf-8 -*-
import base64
import io
import xlsxwriter
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo import http, fields
from odoo.http import request, content_disposition
from odoo.tools import format_date, get_lang


class CustomerPortalEx(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        if 'pricelist_count' in counters:
            if partner.property_product_pricelist and partner.allow_pricelist_download:
                pricelist_count = 1
            else:
                pricelist_count = 0
            values.update({'pricelist_count': pricelist_count})
        return values

    @http.route(['/my/product-pricelist'], type='http', auth="user", website=True)
    def portal_my_product_pricelist(self, **kw):
        partner = request.env.user.partner_id
        if partner.property_product_pricelist and partner.allow_pricelist_download:
            categories = request.env["product.public.category"].search_read([], ["id", "name"])
            values = {"page_name": "product_pricelist", "ecom_categories": categories}
            return request.render("pricelist_portal_download.portal_product_pricelist_page", values)
        else:
            return request.render('website.page_404')

    @http.route("/customer/pricelist", type="http", auth="user", website=True, methods=['POST'])
    def get_customer_pricelist(self, **post):
        partner = request.env.user.partner_id
        if partner.property_product_pricelist and partner.allow_pricelist_download:
            pricelist_file_type = post.get("pricelist_file_type")
            pricelist_product_categ = post.get("pricelist_product_categ")
            values_to_render = {'report_type': 'pdf'}
            ICP = request.env['ir.config_parameter'].sudo().get_param
            show_barcode_in_pricelist = ICP("pricelist_portal_download.show_barcode_in_pricelist")
            show_stock_in_pricelist = ICP("pricelist_portal_download.show_stock_in_pricelist")
            values_to_render.update({"show_stock_in_pricelist": show_stock_in_pricelist, "show_barcode_in_pricelist": show_barcode_in_pricelist})
            if pricelist_product_categ:
                e_com_categ = request.env["product.public.category"].browse(int(pricelist_product_categ))
                e_com_categ_self_child = e_com_categ + e_com_categ.child_id
                pricelist_products = partner.get_pricelist_rules(e_com_categ_self_child.ids)
                values_to_render.update(e_com_categ=e_com_categ)
            else:
                pricelist_products = partner.get_pricelist_rules()
            values_to_render.update(pricelist_products=pricelist_products, currency_id=partner.property_product_pricelist.currency_id, current_date=format_date(request.env, fields.Datetime.now(), lang_code=get_lang(request.env).code))
            if pricelist_file_type == "pdf":
                report = request.env['ir.actions.report']._render_qweb_pdf("pricelist_portal_download.product_pricelist_action_report", data=values_to_render)[0]
                filename = "Product Pricelist - " + fields.Datetime.now().strftime("%Y/%m/%d") + ".pdf"
                content_type = ('Content-Type', 'application/pdf')
                disposition_content = ('Content-Disposition', content_disposition(filename))
                return request.make_response(report, [content_type, disposition_content])
            elif pricelist_file_type == "excel":
                report = self.render_excel_pricelist(values_to_render)
                file_content = base64.b64decode(report or "")
                filename = "Product Pricelist - " + fields.Datetime.now().strftime("%Y/%m/%d") + ".xlsx"
                content_type = ('Content-Type', 'application-/octet-stream')
                disposition_content = ('Content-Disposition', content_disposition(filename))
                return request.make_response(file_content, [content_type, disposition_content])
        else:
            return request.render('website.page_404')

    def render_excel_pricelist(self, values_to_render):
        target_stream = io.BytesIO()
        workbook = xlsxwriter.Workbook(target_stream)
        worksheet = workbook.add_worksheet("Product Pricelist")
        head_format = workbook.add_format({'valign': 'vcenter', 'align': 'center', 'bold': True, 'bg_color': 'gray'})
        head_format_center = workbook.add_format({'valign': 'vcenter', 'align': 'center', 'bold': True, 'bg_color': 'yellow'})
        head_format_left = workbook.add_format({'valign': 'vcenter', 'bold': True, })
        format_right = workbook.add_format({'valign': 'vcenter', 'bold': True, 'align': 'right'})
        format_center = workbook.add_format({'valign': 'vcenter', 'bold': False, 'align': 'center'})
        table_row = 5
        for i in range(7):
            worksheet.set_column(0, i, 20)
        if values_to_render.get("pricelist_products"):
            col_ = 4
            if values_to_render.get("show_stock_in_pricelist"):
                col_ += 1
            if values_to_render.get("show_barcode_in_pricelist"):
                col_ += 1
            worksheet.merge_range(0, 0, 1, col_, "Product Pricelist", head_format_center)
            worksheet.write(2, col_, "Date: " + values_to_render["current_date"], head_format_left)
            if values_to_render.get("e_com_categ"):
                worksheet.write(2, 0, "Product Category: " + values_to_render["e_com_categ"].name, head_format_left)
            worksheet.set_column('E:F', 30)
            worksheet.set_column('C:C', 40)
            h_col = 0
            worksheet.write(4, h_col, 'Internal Ref.', head_format)
            h_col += 1
            if values_to_render.get("show_barcode_in_pricelist"):
                worksheet.write(4, h_col, 'Barcode', head_format)
                h_col += 1
            worksheet.write(4, h_col, 'Product Name', head_format)
            h_col += 1
            worksheet.write(4, h_col, 'Min. Quantity', head_format)
            h_col += 1
            worksheet.write(4, h_col, 'Price Duration', head_format)
            h_col += 1
            worksheet.write(4, h_col, 'Price', head_format)
            h_col += 1
            if values_to_render.get("show_stock_in_pricelist"):
                worksheet.write(4, h_col, 'On Hand Qty.', head_format)
            for pricelist_product in values_to_render.get("pricelist_products"):
                r_col = 0
                worksheet.write(table_row, r_col, pricelist_product['product_id'].default_code or "")
                r_col += 1
                if values_to_render.get("show_barcode_in_pricelist"):
                    worksheet.write(table_row, r_col, pricelist_product['product_id'].barcode or "")
                    r_col += 1
                worksheet.write(table_row, r_col,pricelist_product['product_id'].with_context(display_default_code=False).display_name)
                r_col += 1
                worksheet.write(table_row, r_col, pricelist_product['min_qty'] or "-", format_center)
                r_col += 1
                worksheet.write(table_row, r_col, pricelist_product['price_duration'], format_center)
                r_col += 1
                worksheet.write(table_row, r_col, pricelist_product['price'], format_right)
                r_col += 1
                if values_to_render.get("show_stock_in_pricelist"):
                    if pricelist_product['show_product_stock']:
                        worksheet.write(table_row, r_col, pricelist_product['stock_on_hand'], format_center)
                    else:
                        if pricelist_product['stock_on_hand'] > 0:
                            worksheet.write(table_row, r_col, "In Stock", format_center)
                        else:
                            worksheet.write(table_row, r_col, "Out Of Stock", format_center)
                table_row += 1
        else:
            worksheet.merge_range(0, 0, 1, 6, "You do not have any products in the pricelist!", head_format_left)
        workbook.close()
        target_stream.seek(0)
        output = base64.encodebytes(target_stream.read())
        return output