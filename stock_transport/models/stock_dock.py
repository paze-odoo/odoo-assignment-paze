# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields

class StockDock(models.Model):
    _name = 'stock.dock'
    _description = 'Stock Dock'

    name = fields.Char(string='Dock Name')

    _sql_constraints = [
        ('dock_unique_name', 'UNIQUE(name)', 'Dock Name must be unique.'),
    ]
