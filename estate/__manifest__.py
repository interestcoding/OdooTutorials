# -*- coding: utf-8 -*-
{
    'name': "Real Estate",

    'summary': """
        https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/02_newapp.html
    """,

    'description': """
        https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/02_newapp.html
    """,

    'author': "Odoo",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials/RealEstate',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'assets': {},
    'license': 'AGPL-3'
}