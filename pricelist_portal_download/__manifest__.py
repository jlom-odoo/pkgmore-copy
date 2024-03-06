# -*- coding: utf-8 -*-
{
    'name': "Product Pricelist Portal Download",
    'summary': """Download Pricelist in  PDF or Excel format""",
    'author': 'Azkob',
    'category': 'Website',
    'version': '1.4',
    'website': 'https://www.azkob.com/',
    'depends': ['website_sale_stock', 'sale_management'],
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'reports/product_pricelist_report_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'pricelist_portal_download/static/src/js/portal.js',
            'pricelist_portal_download/static/src/js/pricelist_download.js',
        ],
    },
    'installable': True,
    'application': True,
}