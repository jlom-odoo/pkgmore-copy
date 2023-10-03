{
    'name': "Package More: attach delivery slip along with invoice",
    'summary':
        """
        Module to attach the delivery slip along with invoice on an email. 
        """,
    'description':
        """
        Module to attach the delivery slip along with invoice on an email.
        The delivery slips are created when the user clicks on "Validate" (stock.picking).
        To retrieve each delivery slip from account.move, we include a field called invoice_origin on ir_attachment.py
        These delivery slips are attached to mail.template, which generates and sends the email.
        Developer: ralb
        Task ID: 3459183
        Link to task: https://www.odoo.com/web#id=3459183&cids=17&menu_id=4720&action=333&active_id=360&model=project.task&view_type=form
        """,
    'author': "Odoo Inc.",
    'license': 'OPL-1',
    'website': "https://www.odoo.com",
    'category': 'Custom Modules',
    'version': '1.0.0',
    'depends': [
        'account',
        'stock',
        'sale',
        'sale_management',
        'account_accountant',
        'purchase',
        'mail',
        'stock_dropshipping'
    ],
}
