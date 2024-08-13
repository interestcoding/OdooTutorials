# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil import relativedelta

from odoo import api
from odoo import fields
from odoo import models
from odoo.exceptions import UserError


class Property(models.Model):
    _name = "estate.property"
    _description = "https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/03_basicmodel.html"

    def _default_date_availability(self):
        return fields.Date.today() + relativedelta.relativedelta(months=3)

    name = fields.Char(required=True, string='Title')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=_default_date_availability, string='Available From')
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_price = fields.Float(compute='_compute_best_price', string='Best Offer')
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')],
        help="garden orientation selection"
    )
    total_area = fields.Integer(compute='_compute_total_area', string='Total Area (sqm)')
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Status',
        selection=[
            ('New', 'New'),
            ('Offer Received', 'Offer Received'),
            ('Offer Accepted', 'Offer Accepted'),
            ('Sold', 'Sold'),
            ('Canceled', 'Canceled'),
        ],
        help="state selection",
        default='New'
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesperson_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for line in self:
            line.total_area = line.living_area + line.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for line in self:
            line.best_price = max(line.offer_ids.mapped('price')) if line.offer_ids else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'North'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_set_property_sold(self):
        for record in self:
            if record.state == 'Canceled':
                raise UserError('Canceled properties cannot be sold.')
            record.state = 'Sold'
        return True

    def action_set_property_canceled(self):
        for line in self:
            if line.state == 'Sold':
                raise UserError('Sold properties cannot be canceled.')
            line.state = 'Canceled'
        return True
