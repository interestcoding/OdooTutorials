# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, Command
from odoo import models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_property_sold(self):

        # 获取当前物业的 partner_id
        partner = self.buyer_id  # 假设你的模型中有一个 buyer_id 字段

        # 计算费用
        sale_fee = self.selling_price * 0.06
        admin_fee = 100.00

        # 创建发票所需的字段值
        invoice_values = {
            'partner_id': partner.id,  # 这是发票的客户
            'move_type': 'out_invoice',  # 这是客户发票类型
            'invoice_date': fields.Date.today(),  # 可以选择设置发票日期
            'invoice_line_ids': [
                Command.create({
                    'name': 'Sales Fee (6% of selling price)',
                    'quantity': 1,
                    'price_unit': sale_fee,
                }),
                Command.create({
                    'name': 'Administrative Fee',
                    'quantity': 1,
                    'price_unit': admin_fee,
                })
            ],
        }

        # 创建一个新的会计凭证
        self.env['account.move'].create(invoice_values)

        return super().action_set_property_sold()
