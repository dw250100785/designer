# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import openerp.addons.decimal_precision as dp

from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time

class account_analytic_account(osv.osv):
    """ 扩展发票管理"""
    _name = "account.analytic.account"
    _inherit = ['account.analytic.account']
    _columns = {
        'contract_type': fields.many2one('designer.contract.type',string='合同类型', required=True),
        'contract_amount': fields.float('合同金额', digits_compute=dp.get_precision('invoice_amount'),required=True),
        'contract_amount_big': fields.char('合同金额大写', required=True),
        'project_ids': fields.many2one('designer.project', string='项目简报'),
        'card_line': fields.one2many('designer.contract.rule.line', 'card_id', '付款方式'),

    }

    _defaults = {

    }


class designer_contract_rule_line(osv.osv):
    """ 项目工作卡物料管理"""
    _name = 'designer.contract.rule.line'
    _inherit = ['mail.thread']
    _columns = {
        'card_id': fields.many2one('account.analytic.account', '工作卡', ondelete='cascade', select=True),
        'line_no': fields.integer('次数', required=True,change_default=True, select=True, track_visibility='always'),
        'percentage': fields.float('比例',digits_compute= dp.get_precision('Price'), required=True, change_default=True, select=True, track_visibility='always'),
        'price': fields.float('金额',digits_compute= dp.get_precision('Price'), required=True, change_default=True, select=True, track_visibility='always'),
        'note': fields.text('里程碑',size=64,change_default=True, select=True, track_visibility='always'),
    }
    _sql_constraints = [
        ('line_no', 'unique(line_no)', 'The name of the idea must be unique')
    ]
    _defaults = {
     #   'line_no': 1,
    }
    _order = 'line_no asc'

