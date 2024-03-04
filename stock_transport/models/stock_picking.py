# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    volume = fields.Float(compute='_cal_volume', digits='Stock Volume', help="Total volume of the products in the picking")
    weight = fields.Float(compute='_cal_weight', digits='Stock Weight', help="Total weight of the products in the picking")

    @api.depends('move_ids')
    def _cal_volume(self):
        for picking in self:
            picking.volume = sum(move.product_id.volume * move.quantity for move in picking.move_ids if move.state != 'cancel')

    @api.depends('move_ids')
    def _cal_weight(self):
        for picking in self:
            picking.weight = sum(move.product_id.weight * move.quantity for move in picking.move_ids if move.state != 'cancel')
