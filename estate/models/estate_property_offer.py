# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/07_relations.html"

    price = fields.Float()
    status = fields.Selection(
        selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
