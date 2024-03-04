# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from datetime import timedelta

class StockPickingBatchExtension(models.Model):
    _inherit = 'stock.picking.batch'

    dock_id = fields.Many2one('stock.dock', string='Dock')
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle')
    vehicle_category_id = fields.Many2one('fleet.vehicle.model.category', string='Vehicle Category')
    weight = fields.Float(string='Weight', compute='_compute_weight', store=True)
    volume = fields.Float(string='Volume', compute='_compute_volume', store=True)
    date_from = fields.Date('Date From', required=True, index=True, default=fields.Date.today)
    date_to = fields.Date('Date To', required=True, index=True, default=lambda self: fields.Date.today() + timedelta(days=2))

    # @api.depends('picking_ids', 'vehicle_category_id','move_line_ids.product_id.weight', 'move_ids.quantity', 'move_ids')
    @api.depends('picking_ids','picking_ids.move_line_ids.product_id.weight','vehicle_category_id')
    def _compute_weight(self):
        for batch in self:
            if batch.vehicle_category_id:
                batch.weight = (sum(picking.weight for picking in batch.picking_ids) / batch.vehicle_category_id.max_weight) * 100
            else:
                batch.weight = 0.0

    @api.depends('picking_ids', 'picking_ids.move_line_ids.product_id.volume', 'vehicle_category_id')
    def _compute_volume(self):
        for batch in self:
            if batch.vehicle_category_id:
                batch.volume = (sum(picking.volume for picking in batch.picking_ids) / batch.vehicle_category_id.max_volume) * 100
            else:
                batch.volume = 0.0

    @api.depends('name', 'weight', 'volume')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.name} {record.weight:.0f}kg, {record.volume:.0f}m\u00B3 {record.vehicle_id.driver_id.name or ''}"