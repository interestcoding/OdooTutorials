# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/07_relations.html'
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'A property tag name must be unique.')
    ]
