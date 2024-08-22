# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime

from dateutil import relativedelta

from odoo import api
from odoo import fields
from odoo import models
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/07_relations.html'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7, string='Validity (days)')
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'An offer price must be strictly positive.')
    ]

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for line in self:
            if line.create_date:
                line.date_deadline = line.create_date + relativedelta.relativedelta(days=line.validity)
            else:
                line.date_deadline = datetime.now() + relativedelta.relativedelta(days=line.validity)

    @api.model
    def create(self, vals):
        # 检查新报价是否低于现有报价
        existing_offers = self.search([('property_id', '=', vals['property_id'])])
        if existing_offers and vals['price'] < max(existing_offers.mapped('price')):
            raise UserError('It should not be possible to create an offer with a lower price than an existing offer.')
        property_obj = self.env['estate.property'].browse(vals['property_id'])
        property_obj.state = 'offer received'
        return super().create(vals)

    def _inverse_date_deadline(self):
        for line in self:
            line.validity = (line.date_deadline - line.create_date.date()).days

    def action_accept_property_offer(self):
        for line in self:
            if line.property_id.state == 'offer accepted':
                raise UserError('Only one offer can be accepted for a given property.')
            line.status = 'accepted'
            line.property_id.selling_price = line.price
            line.property_id.buyer_id = line.partner_id
            line.property_id.state = 'offer accepted'
        return True

    def action_refuse_property_offer(self):
        for line in self:
            if line.status == 'accepted':
                line.property_id.selling_price = 0
                line.property_id.buyer_id = None
            line.status = 'refused'
        return True
