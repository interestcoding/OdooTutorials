# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields
from odoo import models
from odoo import api


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/07_relations.html'
    _order = 'name'

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')
    sequence = fields.Integer('Sequence', default=1, help='Used to order types.')

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'A property type name must be unique.')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for line in self:
            line.offer_count = len(line.offer_ids)
