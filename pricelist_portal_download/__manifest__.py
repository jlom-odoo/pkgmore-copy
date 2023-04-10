# -*- coding: utf-8 -*-
{
    'name': "Product Pricelist Portal Download",

    'summary': """Download Pricelist in  PDF or Excel format""",

    'description': """
  This module will help you to allow your selected customer to download their pricelist
                                for products.
                                You can also control that a customer can see the available product stock or just see the
                                stock status.
                                Customer can download the pricelist in PDF and Excel format. They can also filter the
                                pricelist by product category.
                                In the product pricelist we are showing all important details like the minimum quantity
                                to buy to get the offer or the time duration in which they have to buy a product to get
                                the offer price. This will be a helpful tool for a B2B and B2C business    """,

    'author': 'Azkob',
    'category': 'Website',
    'version': '1.0',
    'website': 'https://www.azkob.com/',
    # any module necessary for this one to work correctly
    'depends': ['website_sale_stock', 'sale_management'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'reports/product_pricelist_report_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'pricelist_portal_download/static/src/js/portal.js',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
    ],
    'images': [
        'static/description/banner.jpg',
    ],
    'installable': True,
    'application': True,
    'price': 55,
    'currency': 'EUR',
    'live_test_url': "https://youtu.be/eMXeZWETqlM",
}
