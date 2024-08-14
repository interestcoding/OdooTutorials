# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/07_relations.html"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'A property type name must be unique.')
    ]
