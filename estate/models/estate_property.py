# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil import relativedelta

from odoo import fields, models


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
