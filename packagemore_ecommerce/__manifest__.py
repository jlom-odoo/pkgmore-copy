
{
    'name': 'Packagemore Ecommerce',

    'summary': 'Restrictions on ecommerce views',

    'description': """
    Task ID: 3108813
    Written by: jden

    Only portal users are able to reach checkout.
    Products now have an extra field "exclusive_customer". If this field is set, only that customer will
    be able to view that product in the shop.
    """,

    'author': 'Odoo',
    'website': 'https://www.odoo.com/',

    'category': 'Custom Development',
    'version': '1.0',
    'license': 'OPL-1',
    'depends': ['website_sale', 'contacts', 'sale_management'],
    'data': [
        'views/product_template_views.xml'
    ],
}
