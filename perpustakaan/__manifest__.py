# -*- coding: utf-8 -*-
{
    'name': "Library Ubhara Jaya",

    'summary': """Ubhara Jaya Library""",

    'description': """
        Perpustakaan module for managing books:
            - Perpustakaan courses
    """,

    'author': "Ubhara Jaya",
    'website': "http://www.ubharajaya.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/res_partner_views.xml',
        'views/product_views.xml',
        'views/perpustakaan_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
