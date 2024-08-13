# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime

from dateutil import relativedelta

from odoo import api
from odoo import fields
from odoo import models


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
    validity = fields.Integer(default=7, string='Validity (days)')
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse="_inverse_date_deadline")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for line in self:
            if line.create_date:
                line.date_deadline = line.create_date + relativedelta.relativedelta(days=line.validity)
            else:
                line.date_deadline = datetime.now() + relativedelta.relativedelta(days=line.validity)

    def _inverse_date_deadline(self):
        for line in self:
            line.validity = (line.date_deadline - line.create_date.date()).days
