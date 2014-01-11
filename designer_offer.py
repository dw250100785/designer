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

class designer_offer(osv.osv):
    """ 自定义的报价单"""
    _name = "designer.offer"
    _description = u'报价单'
    _inherit = ['mail.thread']
    _columns = {
        'work_id': fields.many2one('designer.card', '所属工作卡', change_default=True, select=True, track_visibility='always'),
        'name': fields.char('单号', size=64, required=True, select=True, help="Unique number of the purchase order, computed automatically when the purchase order is created."),
        'partner_id':fields.many2one('res.partner', '制作部', required=True,
            change_default=True, track_visibility='always'),
        'project_ids': fields.many2one('designer.project', string='项目简报'),
        'date_order':fields.date('日期', required=True, select=True, help="Date on which this document has been created."),
        'card_line': fields.one2many('designer.offer.line', 'card_id', '物料清单'),
        'state': fields.selection([
            ('draft', '草稿中'),
            ('open', '已提交'),
            ('verify1', '一次确认'),
            ('verify2', '二次确认'),
            ('cancel', '已拒绝')],
            '状态', readonly=True, track_visibility='onchange',
        ),
    }

    _rec_name = 'name'
    _sql_constraints = [
    ]
    _defaults = {
         'date_order': fields.date.context_today,
         'state': lambda *a: 'draft',
         'name': lambda obj, cr, uid, context: '/',
    }
    _order = 'name asc'

    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'designer.offer') or '/'
        offer =  super(designer_offer, self).create(cr, uid, vals, context=context)
        return offer

    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'state':'draft',
            'name': self.pool.get('ir.sequence').get(cr, uid, 'designer.offer'),
        })
        return super(designer_offer, self).copy(cr, uid, id, default, context)


    def designer_offer_draft(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)

    def designer_offer_cancel1(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)

    def designer_offer_cancel2(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)

    def designer_offer_open(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'open'}, context=context)

    def designer_offer_verify1(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'verify1'}, context=context)

    def designer_offer_verify2(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'verify2'}, context=context)

class designer_offer_line(osv.osv):
    """ 项目工作卡物料管理"""
    _name = 'designer.offer.line'
    _inherit = ['mail.thread']

    def on_change_price(self, cr, uid, ids, number,price, context=None):
        if not number:
            return {}
        #odometer_unit = self.pool.get('fleet.vehicle').browse(cr, uid, vehicle_id, context=context).odometer_unit
        return {
            'value': {
                'subprice': number*price,
            }
        }

    def _get_seq(self, cr, uid, ids, context=None):
        return self.pool.get('ir.sequence').get(cr, uid, 'designer.offer.line')

    _columns = {
        'card_id': fields.many2one('designer.offer', '工作卡', ondelete='cascade', select=True),
        'line_no': fields.char('编号', required=True,change_default=True, select=True, track_visibility='always'),
        'project_request': fields.text('项目要求', size=64, required=True, change_default=True, select=True, track_visibility='always'),
        'number': fields.integer('数量', required=True, change_default=True, select=True, track_visibility='always'),
        'price': fields.float('价格',digits_compute= dp.get_precision('Price'), required=True, change_default=True, select=True, track_visibility='always'),
        'subprice': fields.float('总价', required=True, change_default=True, select=True, track_visibility='always'),
        'note': fields.text('备注',size=64,change_default=True, select=True, track_visibility='always'),
    }
    _sql_constraints = [
        ('line_no', 'unique(line_no)', '此编号已被占用')
    ]
    _defaults = {
        'line_no':_get_seq
    }
    _order = 'line_no asc'
