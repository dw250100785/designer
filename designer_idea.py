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

class designer_idea(osv.osv):
    """ 创意简报"""
    _name = 'designer.idea'
    _description = "designer_idea"
    _inherit = ['mail.thread']
    _columns = {
        'file_id': fields.many2one('ir.attachment', '客户签字', required=False, select=1),
        'work_id': fields.many2one('designer.card', '所属工作卡', change_default=True, select=True, track_visibility='always'),
        #'create_uid': fields.many2one('res.users','撰写人', required=True, readonly=True,states={'draft': [('readonly', False)]}),
        'name': fields.char('创意简报', size=64, required=True, ),
        'brand_id': fields.many2one('designer.brand', '品牌', required=True, change_default=True, select=True, track_visibility='always'),
        #取自工作卡
        'partner_id':fields.related(
             'work_id',#关联字段
             'partner_id',#项目简报的
             string='客户',
             type='many2one',
             relation='res.partner',
             readonly=True,
             store=True
        ),
       # 'partner_id': fields.many2one('res.partner', '客户', required=True, change_default=True, select=True, track_visibility='always'),
        #'product_id': fields.many2one('product.product', '产品', readonly=True, required=True, change_default=True, select=True,states={'draft': [('readonly', False)]}),
        'date':fields.date('日期',required=True,track_visibility='onchange',),
        'end_time':fields.date('完稿时间',track_visibility='onchange',),
        'brand_definition': fields.text('品牌定义', help='品牌定义',track_visibility='onchange', ),
        'marketing_problem_definition': fields.text('行销问题', help='行销问题',track_visibility='onchange',),
        'role_and_aim_of_advertising': fields.text('广告的角色和意图', help='广告的角色和意图',track_visibility='onchange',),
        'competition_scope': fields.text('竞争范畴', help='竞争范畴',track_visibility='onchange', ),
        'target_segment_and_its_current_situation': fields.text('目标对象及其现状', help='目标对象及其现状',track_visibility='onchange',),
        'impact_of_advertising_you_want': fields.text('期望广告对消费者有何影响', help='期望广告对消费者有何影响',track_visibility='onchange',),
        'adverting_information_and_brand_proposition': fields.text('广告信息或品牌主张', help='广告信息或品牌主张',track_visibility='onchange',),
        'critical_support': fields.text('重要支持', help='重要支持', track_visibility='onchange',),
        'necessary_information': fields.text('必要事项', help='必要事项',track_visibility='onchange',),
        'advertising_tone': fields.text('广告格调', help='广告格调',track_visibility='onchange',),
        'background_information_concerned': fields.text('相关背景资料', help='相关背景资料',track_visibility='onchange',),
        #'receiver_uid':fields.many2one('res.users','我方对接人', required=True, readonly=True ,states={'draft': [('readonly', False)]}),
        'project_ids': fields.many2one('project.project', string='项目',track_visibility='onchange',),
        'state': fields.selection([('draft', '草稿中'),
            ('open', '已提交'),
            ('confirmed', '已审核'),
            ('verify1', '确认(1)通过'),
            ('verify2', '确认(2)通过'),
            ('cancel', '已拒绝'),
            ('done', '已完成')],
            '状态', readonly=True, track_visibility='onchange',
            help='总监审核，并创建提案ppt.\
            \nae第一次确认并给客户签字.\
            \n 第二次确认完稿时间.'
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
       # ('name', 'unique(name)', 'The name of the idea must be unique')
    ]
    _defaults = {
        'state': lambda *a: 'draft',
    }
    _order = 'name asc'

    def designer_idea_draft(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)

    def designer_idea_submit(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'open'}, context=context)

    def designer_idea_confirmed(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'confirmed'}, context=context)

    def designer_idea_verify1(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'verify1'}, context=context)

    def designer_idea_verify2(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'done'}, context=context)

    def designer_idea_cancel(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)


