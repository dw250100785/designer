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

import pdb #debug

class designer_bill(osv.osv):
    """ 发票管理"""
    _name = "designer.bill"
    _inherit = ['mail.thread','ir.attachment']

    _columns = {
        'work_id': fields.many2one('designer.card', '所属工作卡', change_default=True, select=True, track_visibility='always'),
        'partner_id':fields.many2one('res.partner', '客户', required=True,
            change_default=True, track_visibility='always'),
        'invoice_head': fields.char('发票抬头', size=64, required=True),
        'date':fields.datetime('日期',required=True),
        'invoice_amount': fields.float('金额', digits_compute=dp.get_precision('invoice_amount'),required=True),
        'project_ids': fields.many2one('designer.project', string='项目简报'),
        'state_apply': fields.selection(
            [('true', '是'),
            ('false', '否')],
            '申请',track_visibility='onchange',
        ),
        'state_make_out': fields.selection(
            [('true', '是'),
            ('false', '否')],
            '开票',track_visibility='onchange',
        ),
        'state_draw': fields.selection(
            [('true', '是'),
            ('false', '否')],
            '领取', track_visibility='onchange',
        ),
        'state_arrive': fields.selection(
            [('true', '是'),
            ('false', '否')],
            '到账',track_visibility='onchange',
        ),
        'state': fields.selection([
            ('draft', '草稿中'),
            ('send', '已提交申请'),
            ('makeout', '已开出'),
            ('refuse', '已拒绝'),
            ('accept', '已领取'),
            ('done', '已确认')],
            '状态', readonly=True, track_visibility='onchange',
        )

    }
    _rec_name = 'invoice_head'

    _order = 'id desc'

    _defaults = {
        'state': lambda *a: 'draft',
        'state_apply': 'false',
        'state_make_out': 'false',
        'state_draw': 'false',
        'state_arrive': 'false',
    }

    def designer_bill_draft(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)

    def designer_bill_send(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'send','state_apply': 'true'}, context=context)


    def designer_bill_notifer(self, cr, uid, ids, context=None):
        #current user id    uid
        #list of ids    ids
        #id -- id of the record to copy
        pdb.set_trace()
        #print id
        #oe方法第三个参数一般是查询参数

        records = self._get_followers(cr, uid, ids, None, None, context=context)
        followers = records[ids[0]]['message_follower_ids']
        self.message_post(
            cr,
            uid,
            ids,
            body='发票已经开出',
            subtype='mt_comment',
            partner_ids=followers,
            context=context
        )


        post_vars = {
            'subject': "Message subject",
            'body': "Message body",
            'partner_ids': [(4, ids[0].create_uid.partner_id)],
            }
            # Where "4" adds the ID to the list
            # of followers and "3" is the partner ID
        thread_pool = self.pool.get('mail.thread')
        thread_pool.message_post(
                cr, uid, False,
                type="notification",
                subtype="mt_comment",
                context=context,
                **post_vars)

        self.message_post(cr, uid, id,
                _("发票已经开出，请确认."), context=context)


    def designer_bill_notifer11(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)
#开出
    def designer_bill_makeout(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'makeout','state_make_out': 'true'}, context=context)
#开出  拒绝
    def designer_bill_refuse(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'refuse','state_make_out':'false'}, context=context)
#领取
    def designer_bill_accept(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'accept','state_draw': 'true'}, context=context)
#确认
    def designer_bill_done(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'done','state_arrive': 'true'}, context=context)
