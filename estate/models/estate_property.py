# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil import relativedelta

from odoo import api
from odoo import fields
from odoo import models
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from odoo.tools import float_is_zero
from odoo.tools import float_compare


class Property(models.Model):
    _name = 'estate.property'
    _description = 'https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/03_basicmodel.html'
    _order = 'id desc'

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
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="garden orientation selection"
    )
    total_area = fields.Integer(compute='_compute_total_area', string='Total Area (sqm)')
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Status',
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        help="state selection",
        default='new'
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesperson_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tag")
    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'A property expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'A property selling price must be positive.')
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for line in self:
            if not float_is_zero(line.selling_price, precision_rounding=0.01):
                min_selling_price = line.expected_price * 0.9
                if float_compare(line.selling_price, min_selling_price, precision_rounding=0.01) < 0:
                    raise ValidationError('The selling price cannot be lower than 90% of the expected price.')

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
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        if any(line.state not in ['new', 'canceled'] for line in self):
            raise UserError('It should not be possible to delete a property which is not new or canceled.')

    def action_set_property_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('Canceled properties cannot be sold.')
            record.state = 'sold'
        return True

    def action_set_property_canceled(self):
        for line in self:
            if line.state == 'sold':
                raise UserError('Sold properties cannot be canceled.')
            line.state = 'canceled'
        return True
