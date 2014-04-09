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
from lxml import etree
import openerp.addons.decimal_precision as dp

from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time
from openerp.addons.workflow_info import workflow_func


class designer_order(osv.osv):
    """ 工单"""
    _name = 'designer.order'
    _description = "designer_order"
    _inherit = ['mail.thread']

    def _get_seq(self, cr, uid, ids, context=None):
        return self.pool.get('ir.sequence').get(cr, uid, 'designer.order')

    _columns = {
        'file_id': fields.many2one('ir.attachment', '客户签字', required=False, select=1),
        'work_id': fields.many2one('designer.card', '所属工作卡', change_default=True, select=True, track_visibility='always'),
        'name': fields.char('工单编号', required=True,track_visibility='always'),
        'order_line': fields.one2many('designer.order.line', 'order_id', '制作明细',track_visibility='always' ),
        'project_id': fields.many2one('designer.project', string='项目简报',track_visibility='always'),

        #取自工作卡
        'partner_id': fields.related(
            'work_id', #关联字段
            'partner_id', #工作卡对象字段
            string='客户',
            type='many2one',
            relation='res.partner',
            readonly=True,
            store=True
        ),
        # 'partner_id':fields.related(
        #     'project_id',#关联字段
        #     'partner_id',#项目简报的
        #     string='客户',
        #     type='many2one',
        #     relation='res.partner',
        #     readonly=True,
        #     store=True
        #  ),
        'state': fields.selection([
            ('draft', '草稿中'),
            ('open', '已批准'),
            ('verify1', '一次确认'),
            ('verify2', '二次确认'),
            ('cancel', '已拒绝')],
            '状态', readonly=True, track_visibility='onchange',
        ),
        'project_type': fields.selection([('print', '印刷'),
            ('logo', 'LOGO'),
            ('ad', '广告'),],
            '项目类型', track_visibility='onchange',
        ),
        #工作流审批以及记录
        'wkf_logs':fields.function(
            workflow_func._get_workflow_logs,
            string='审批记录',
            type='one2many',
            relation="workflow.logs",
            readonly=True),
    }
    _rec_name = 'name'
    _sql_constraints = [
        ('order_no', 'unique(order_no)', u'工单编号必须唯一')
    ]
    _defaults = {
        'state': lambda *a: 'draft',
        'name':_get_seq
    }
    _order = 'name asc'



    def designer_order_draft(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)

    def designer_order_cancel1(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)

    def designer_order_cancel2(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)

    def designer_order_open(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'open'}, context=context)

    def designer_order_verify1(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'verify1'}, context=context)

    def designer_order_verify2(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'verify2'}, context=context)


class designer_order_line(osv.osv):
    """ 工单制作明细"""
    _name = 'designer.order.line'
    _inherit = ['mail.thread']
    _columns = {
        'order_id': fields.many2one('designer.order', '工单', ondelete='cascade', select=True),#关联id
        'line_no': fields.char('编号', required=True,change_default=True, select=True, track_visibility='always'),
        #'project_request': fields.text('项目要求', size=64, required=True, change_default=True, select=True, track_visibility='always'),
        'number': fields.integer('数量', required=True, change_default=True, select=True, track_visibility='always'),
        'p_number': fields.integer('P数', required=True, change_default=True, select=True, track_visibility='always'),
        'size': fields.float('尺寸',digits_compute= dp.get_precision('Price'), required=True, change_default=True, select=True, track_visibility='always'),
        'face_page': fields.float('封面纸张(g)',digits_compute= dp.get_precision('Price'), required=True, change_default=True, select=True, track_visibility='always'),
        'inside_page': fields.float('内页纸张(g)',digits_compute= dp.get_precision('Price'), required=True, change_default=True, select=True, track_visibility='always'),
        'note': fields.text('备注',size=64,change_default=True, select=True, track_visibility='always'),
        'content': fields.text('项目内容',size=64,change_default=True, select=True, track_visibility='always'),
        'binding_style': fields.char('装订方式',size=64,change_default=True, select=True, track_visibility='always'),
        'other_craft': fields.char('其他工艺',size=64,change_default=True, select=True, track_visibility='always'),
        'date':fields.datetime('交货时间',required=True),
        'print_type': fields.selection([
            ('one', '单'),
            ('both', '双'),
            ('no', '否'),],
            '封面印刷', track_visibility='onchange',
        )
    }
    _sql_constraints = [
       # ('line_no', 'unique(line_no)', 'The name of the idea must be unique')
    ]
    _defaults = {
    }
    _order = 'line_no asc'
