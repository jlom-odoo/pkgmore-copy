{
    "name": "Package More Ecommerce Pricelists",
    "summary": """Package More Ecommerce Pricelists: Show minimum quantity from pricelist""",
    "description": """
        If there is a minimum quantity defined on the pricelist, show the minimum quantity of the product for the selected pricelist on the website.

        Developer: ELCE
        Ticket ID: 3389883
    """,
    "author": "Odoo PS",
    "website": "https://www.odoo.com",
    "category": "Custom Development",
    "version": "1.0",
    "depends": [],
    "data": [
        "views/website_sale_templates.xml"
    ],
    'assets': {
        'web.assets_frontend': [
            'packagemore_ecommerce_pricelists/static/src/scss/package_more_website.scss',
            'packagemore_ecommerce_pricelists/static/src/js/website_sale.js',
        ]
    },
    "license": "OPL-1",
}
