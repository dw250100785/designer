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

from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time
from openerp.addons.workflow_info import workflow_func

class designer_policy(osv.osv):
    """ 创意策略"""
    _name = 'designer.policy'
    _description = "designer_policy"
    _inherit = ['mail.thread']

    def _get_seq(self, cr, uid, ids, context=None):
        return self.pool.get('ir.sequence').get(cr, uid, 'designer.policy')

    _columns = {
        'file_id': fields.many2one('ir.attachment', '客户签字', required=False, select=1),
        'work_id': fields.many2one('designer.card', '所属工作卡', change_default=True, select=True, track_visibility='always'),
        'project_id': fields.many2one('designer.project', string='项目简报',track_visibility='always' ),
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
        #     store=True,
        # ),
        'policy_no': fields.char('编号', size=64, required=True,track_visibility='always'),
        'name': fields.char('名称', size=64, required=True,track_visibility='always'),
        'date': fields.date('日期', help='日期',track_visibility='always'),
        'note': fields.text('备注', help='备注',track_visibility='always'),
        'policy_line': fields.one2many('designer.policy.line', 'line_id', '创意策略', readonly=True, states={'draft':[('readonly',False)]}),
        'state': fields.selection([('draft', '未提交'),
            ('open', '已提交'),
            ('cancel', '已拒绝'),
            ('close', '已完成')],
            '状态', readonly=True, track_visibility='onchange',
        ),
        #工作流审批以及记录
        'wkf_logs':fields.function(
            workflow_func._get_workflow_logs,
            string='审批记录',
            type='one2many',
            relation="workflow.logs",
            readonly=True),
    }
    _sql_constraints = [
       # ('policy_no', 'unique(policy_no)', 'The name of the idea must be unique')
    ]

    _order = 'policy_no asc'

    _defaults = {
        'state': lambda *a: 'draft',
        'policy_no':_get_seq,
        'name':_get_seq,
    }

    def designer_policy_cancel(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)

    def designer_policy_open(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'open'}, context=context)

    def designer_policy_close(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'close'}, context=context)

    def designer_policy_draft(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)

class designer_policy_line(osv.osv):
    """ 创意策略"""
    _name = 'designer.policy.line'
    _inherit = ['mail.thread','ir.attachment']
    _columns = {
        'line_id': fields.many2one('designer.policy', '策略编号', ondelete='cascade', select=True),
        'line_no': fields.char('次数', size=64, required=True),
        'name': fields.char('名称', size=64, required=True),
        'date': fields.date('日期', help='日期'),
        'summary': fields.text('策略概要', help='策略概要'),
        'state': fields.selection([('draft', '草稿中'),
            ('open', '已批准'),
            ('cancel', '已拒绝'),
            ('close', '已完成')],
            '状态', track_visibility='onchange',
        ),
    }
    _sql_constraints = [
        #('line_no', 'unique(line_no)', 'The name of the idea must be unique')
    ]

    _order = 'line_no asc'

    _defaults = {
        'state': lambda *a: 'draft',
    }
