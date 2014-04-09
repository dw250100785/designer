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
# < button
# name = "%(act_designer_card_2_project_project)d"
# string = "项目进度"
# type = "action"
# style = "width:80px;height:24px" / >
#
# < button
# name = "%(act_designer_card_2_designer_project)d"
# string = "项目简报"
# type = "action"
# style = "width:80px;height:24px" / >
#
# < button
# name = "%(act_designer_card_2_designer_idea)d"
# string = "创意简报"
# type = "action"
# style = "width:80px;height:24px" / >
#
# < button
# name = "%(act_designer_card_2_designer_inquiry)d"
# string = "询价单"
# type = "action"
# style = "width:80px;height:24px" / >
#
# < button
# name = "%(act_designer_card_2_designer_offer)d"
# string = "报价单"
# type = "action"
# style = "width:80px;height:24px" / >
#
# < button
# name = "%(act_designer_card_2_designer_agreement)d"
# string = "合同"
# type = "action"
# style = "width:80px;height:24px" / >
#
# < button
# name = "%(act_designer_card_2_designer_bill)d"
# string = "发票"
# type = "action"
# style = "width:80px;height:24px" / >
# < br / >
#
# < button
# name = "%(act_designer_card_2_designer_paper)d"
# string = "竟稿申请"
# type = "action"
# style = "width:100px;height:24px" / >
#
# < button
# name = "%(act_designer_card_2_designer_policy)d"
# string = "创意策略"
# type = "action"
# style = "width:100px;height:24px" / >
#
# < button
# name = "%(act_designer_card_2_designer_order)d"
# string = "工单"
# type = "action"
# style = "width:100px;height:24px" / >
#
# < button
# name = "%(act_designer_card_2_designer_archive)d"
# string = "项目备档单"
# type = "action"
# style = "width:100px;height:24px" / >
#
##############################################################################


from lxml import etree
import openerp.addons.decimal_precision as dp

from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time
from openerp.addons.workflow_info import workflow_func


class designer_card(osv.osv):
    """ 项目工作卡"""
    _name = 'designer.card'
    _description = "designer_card"
    _inherit = ['mail.thread']

    def _get_seq(self, cr, uid, ids, context=None):
        return self.pool.get('ir.sequence').get(cr, uid, 'designer.card')

    """
    工作卡
    工作卡设定 客户以及工作清单其他模块直接取工作卡

    """
    _columns = {
        'file_id': fields.many2one('ir.attachment', '客户签字', required=False, select=1),
        'card_no': fields.char('编号', required=True, readonly=True,states={'draft': [('readonly', False)]}),
        'card_line': fields.one2many('designer.card.line', 'card_id', '工作清单'),
       # 'project_id': fields.many2one('designer.project', string='项目简报',ondelete='cascade'),
       #  'partner_id':fields.related(
       #      'project_id',#关联字段
       #      'partner_id',#项目简报的
       #      string='客户',
       #      type='many2one',
       #      relation='res.partner',
       #      readonly=True,
       #      store=True
       #  ),
        'state': fields.selection([('draft', '草稿中'),
            ('open', '已提交'),
            ('cancel', '已拒绝'),
            ('close', '已完成')],
            '状态', readonly=True, track_visibility='onchange',
        ),
        'partner_id': fields.many2one('res.partner', '客户', required=True,
                                      change_default=True, track_visibility='always'),
        # 'idea_id': fields.many2one('res.users','创意部负责人',),
        # 'design_id': fields.many2one('res.users','设计部负责人',),
        #工作流审批以及记录
        'wkf_logs':fields.function(
            workflow_func._get_workflow_logs,
            string='审批记录',
            type='one2many',
            relation="workflow.logs",
            readonly=True),

        # 关联
        'project_project_ids': fields.one2many('project.project', 'work_id', '项目'),

        'designer_project_ids': fields.one2many('designer.project', 'work_id', '项目简报'),

        'idea_ids': fields.one2many('designer.idea', 'work_id', '创意简报'),

        'inquiry_ids': fields.one2many('designer.inquiry', 'work_id', '询价单'),

        'offer_ids': fields.one2many('designer.offer', 'work_id', '报价单'),

        'agreement_ids': fields.one2many('designer.agreement', 'work_id', '合同'),
        'bill_ids': fields.one2many('designer.bill', 'work_id', '发票'),
        'paper_ids': fields.one2many('designer.paper', 'work_id', '竟稿申请'),
        'policy_ids': fields.one2many('designer.policy', 'work_id', '创意策略'),
        'order_ids': fields.one2many('designer.order', 'work_id', '工单'),
        'archive_ids': fields.one2many('designer.archive', 'work_id', '项目备档单'),
        # 团队成员
        'members': fields.many2many('res.users', 'card_user_rel', 'card_id', 'uid', '团队成员'),

    }
    _rec_name = 'card_no'
    _sql_constraints = [
        ('card_no', 'unique(card_no)', '卡号必须唯一')
    ]
    _defaults = {
        'state': lambda *a: 'draft',
        'card_no':_get_seq,
    }
    _order = 'card_no asc'

    def designer_card_cancel(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)

    def designer_card_open(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'open'}, context=context)

    def designer_card_close(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'close'}, context=context)

    def designer_card_draft(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)


class designer_card_line(osv.osv):
    """ 项目工作卡物料管理"""
    _name = 'designer.card.line'
    _inherit = ['mail.thread']

    def _get_seq(self, cr, uid, ids, context=None):
        return self.pool.get('ir.sequence').get(cr, uid, 'designer.card.line')

    _columns = {
        'card_id': fields.many2one('designer.card', '工作卡', ondelete='cascade', select=True),
        'line_no': fields.char('编号', required=True,change_default=True, select=True, track_visibility='always'),
        'project_request': fields.text('项目要求', size=64, required=True, change_default=True, select=True, track_visibility='always'),
        'number': fields.integer('数量', required=True, change_default=True, select=True, track_visibility='always'),
        'price': fields.float('价格',digits_compute= dp.get_precision('Price'), required=True, change_default=True, select=True, track_visibility='always'),
        'subprice': fields.float('总价', required=True, change_default=True, select=True, track_visibility='always'),
        'note': fields.text('备注',size=64,change_default=True, select=True, track_visibility='always'),
    }
    _sql_constraints = [
    ]
    _defaults = {
       'line_no':_get_seq
    }
    _order = 'line_no asc'


    # 快捷创建

    # invoice_vals = {
    #     'name': order.client_order_ref or '',
    #     'origin': order.name,
    #     'type': 'out_invoice',
    #     'reference': order.client_order_ref or order.name,
    #     'account_id': order.partner_id.property_account_receivable.id,
    #     'partner_id': order.partner_invoice_id.id,
    #     'journal_id': journal_ids[0],
    #     'invoice_line': [(6, 0, lines)],
    #     'currency_id': order.pricelist_id.currency_id.id,
    #     'comment': order.note,
    #     'payment_term': order.payment_term and order.payment_term.id or False,
    #     'fiscal_position': order.fiscal_position.id or order.partner_id.property_account_position.id,
    #     'date_invoice': context.get('date_invoice', False),
    #     'company_id': order.company_id.id,
    #     'user_id': order.user_id and order.user_id.id or False
    # }


    def designer_quick_create_designer_project(self, cr, uid, ids, context=None):
        for card in self.browse(cr, uid, ids, context=context):

            print "======================", str(card)
            project_obj = self.pool.get('designer.project')
            vals = {
                'work_id':card.id,
                'create_id':ids[0],
            }
            return project_obj.create(cr, uid, vals, context=context)



    def designer_quick_create_project_project(self, cr, uid, ids, context=None):
        for card in self.browse(cr, uid, ids, context=context):
            project_obj = self.pool.get('designer.project')
            vals = {
                'work_id': card.id,
                'create_id': ids[0],
            }

        return project_obj.create(cr, uid, vals, context=context)

    def designer_quick_create_designer_idea(self, cr, uid, ids, context=None):
        for card in self.browse(cr, uid, ids, context=context):
            project_obj = self.pool.get('designer.idea')
            vals = {
                'work_id': card.id,
                'create_id': ids[0],
            }

        return project_obj.create(cr, uid, vals, context=context)
    # 询价单
    def designer_quick_create_designer_inquiry(self, cr, uid, ids, context=None):
        for card in self.browse(cr, uid, ids, context=context):
            project_obj = self.pool.get('designer.inquiry')
            lines = {}
            vals = {
                'work_id': card.id,
                'create_id': ids[0],
            }
            id = project_obj.create(cr, uid, vals, context=context)

            num = 1
            for i in range(card.card_line):
                num += 1
                lines.append((0, 0, {'line_no': num ,'project_request': card.card_line.project_request,'number': card.card_line.number}))
                # Notice how we don't pass id_classb value here,
                # it is implicit when we write one2many field
                project_obj.write(cr, uid, [id],{'card_line': lines}, context=context)

        return True

    def designer_quick_create_designer_offer(self, cr, uid, ids, context=None):
        for card in self.browse(cr, uid, ids, context=context):
            project_obj = self.pool.get('designer.offer')
            vals = {
                'work_id': card.id,
                'create_id': ids[0],
            }

        return project_obj.create(cr, uid, vals, context=context)

    def designer_quick_create_designer_agreement(self, cr, uid, ids, context=None):
        for card in self.browse(cr, uid, ids, context=context):
            project_obj = self.pool.get('designer.agreement')
            vals = {
                'work_id': card.id,
                'create_id': ids[0],
            }

        return project_obj.create(cr, uid, vals, context=context)

    def designer_quick_createdesigner_bill(self, cr, uid, ids, context=None):
        for card in self.browse(cr, uid, ids, context=context):
            project_obj = self.pool.get('designer.bill')
            vals = {
                'work_id': card.id,
                'create_id': ids[0],
            }

        return project_obj.create(cr, uid, vals, context=context)

    def designer_quick_create_designer_paper(self, cr, uid, ids, context=None):
        for card in self.browse(cr, uid, ids, context=context):
            project_obj = self.pool.get('designer.paper')
            vals = {
                'work_id': card.id,
                'create_id': ids[0],
            }

        return project_obj.create(cr, uid, vals, context=context)

    def designer_quick_create_designer_policy(self, cr, uid, ids, context=None):
        for card in self.browse(cr, uid, ids, context=context):
            project_obj = self.pool.get('designer.policy')
            vals = {
                'work_id': card.id,
                'create_id': ids[0],
            }

        return project_obj.create(cr, uid, vals, context=context)

    def designer_quick_create_designer_order(self, cr, uid, ids, context=None):
        for card in self.browse(cr, uid, ids, context=context):
            project_obj = self.pool.get('designer.order')
            vals = {
                'work_id': card.id,
                'create_id': ids[0],
            }

        return project_obj.create(cr, uid, vals, context=context)

    def designer_quick_create_designer_archive(self, cr, uid, ids, context=None):
        for card in self.browse(cr, uid, ids, context=context):
            project_obj = self.pool.get('designer.archive')
            vals = {
                'work_id': card.id,
                'create_id': ids[0],
            }

        return project_obj.create(cr, uid, vals, context=context)



    def designer_idea_cancel(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)

    def designer_idea_open(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'open'}, context=context)

    def designer_idea_close(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'close'}, context=context)

    def designer_idea_draft(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)
