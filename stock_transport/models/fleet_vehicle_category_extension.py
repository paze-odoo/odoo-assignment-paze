# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields,models,api

class FleetVehicleModelCategoryExtension(models.Model):
    _inherit = 'fleet.vehicle.model.category'
    _description = 'Fleet Vehicle Model Category Extension'

    max_weight = fields.Float(string='Max Weight', default=1)
    max_volume = fields.Float(string='Max Volume', default=2)

    _sql_constraints = [
        ('check_max_weight', 'CHECK(max_weight > 0)', 'Max Weight must be greater than 0.'),
        ('check_max_volume', 'CHECK(max_volume > 0)', 'Max Volume must be greater than 0.'),
    ]
    @api.depends('name', 'max_weight', 'max_volume')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.name} ({record.max_weight:.0f}kg, {record.max_volume:.0f}m\u00B3)"
