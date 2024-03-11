# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from datetime import timedelta

class StockPickingBatchExtension(models.Model):
    _inherit = 'stock.picking.batch'

    dock_id = fields.Many2one('stock.dock', string='Dock')
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle')
    vehicle_category_id = fields.Many2one('fleet.vehicle.model.category', string='Vehicle Category')
    weight_percentage = fields.Float(string='Weight', compute='_compute_weight', store=True)
    volume_percentage = fields.Float(string='Volume', compute='_compute_volume', store=True)
    total_weight = fields.Float(string='Total Weight', compute='_compute_weight', store=True)
    total_volume =  fields.Float(string='Total Volume',  compute='_compute_volume', store=True)
    date_end = fields.Date('Date To', compute='_compute_date_end', store=True)
    # date_from = fields.Date('Date From', required=True, default=fields.Date.today) #for learning purpose

    # @api.depends('picking_ids', 'vehicle_category_id','move_line_ids.product_id.weight', 'move_ids.quantity', 'move_ids')
    @api.depends('picking_ids','picking_ids.move_ids.product_id.weight','vehicle_category_id')
    def _compute_weight(self):
        for batch in self:
            if batch.vehicle_category_id:
                batch.total_weight = sum(picking.weight for picking in batch.picking_ids)
                batch.weight_percentage = (batch.total_weight / batch.vehicle_category_id.max_weight) * 100
            else:
                batch.weight_percentage = False

    @api.depends('picking_ids', 'picking_ids.move_ids.product_id.volume', 'vehicle_category_id')
    def _compute_volume(self):
        for batch in self:
            if batch.vehicle_category_id:
                batch.total_volume = sum(picking.volume for picking in batch.picking_ids)
                batch.volume_percentage = (batch.total_volume/ batch.vehicle_category_id.max_volume) * 100
            else:
                batch.volume_percentage = False

    @api.depends('name', 'total_weight', 'total_volume')
    def _compute_display_name(self):
        for record in self:
            if record.total_weight and record.total_volume:
                record.display_name = f"{record.name} {record.total_weight:.2f}kg, {record.total_volume:.2f}m\u00B3 {record.vehicle_id.driver_id.name or ''}"
            else:
                record.display_name = record.name

    @api.depends('scheduled_date')
    def _compute_date_end(self):
        for record in self:
            if record.scheduled_date:
                record.date_end = record.scheduled_date + timedelta(days=2)
            else:
                record.date_end = False
