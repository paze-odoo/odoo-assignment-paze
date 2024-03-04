# -*- coding: utf-8 -*-
{
    'name': "stocktransport",
    'summary': "Transport Management System",
    'description': """Transport Management System""",
    'author': "Odoo",
    'category': 'fleet',
    'version': '0.1',
    'depends': ['base', 'fleet', 'stock_picking_batch', 'stock'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',

        'views/fleet_vehicle_model_views_extension.xml',
        'views/stock_picking_batch_form_extension.xml',
    ],
    'installable': True,
    'sequence': 1,
}
