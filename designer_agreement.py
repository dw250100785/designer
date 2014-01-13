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
import logging

import openerp.addons.decimal_precision as dp


from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import math
import time
import workflow_func

_logger = logging.getLogger()
class designer_contract_type(osv.osv):
    """ 品牌"""
    _name = 'designer.contract.type'
    #双引号
    #_description = "Employee"
    _description = u"品牌"
    _columns = {
        'name': fields.char('名称', size=64, required=True),
        'comment': fields.text('备注', help='备注'),
    }
    _sql_constraints = [
        ('name', 'unique(name)', '名称不能重复')
    ]

    _order = 'name asc'



class designer_agreement(osv.osv):
    """ 扩展发票管理"""

    _name = "designer.agreement"
    _description = "designer_agreement"
    _inherit = ['mail.thread','ir.attachment']

    def _get_seq(self, cr, uid, ids, context=None):
        return self.pool.get('ir.sequence').get(cr, uid, 'designer.agreement')
    """
    分期付款，比例必须总和为100
    """

    def create(self, cr, uid, vals, context=None):

        card_lines = vals.get('card_line',[])
        if not card_lines:
            raise osv.except_osv(('错误提示'), ('必须添写付款信息'))
        #调试 最佳实践
        #设断点可以查看传递参数 F7

        #raise osv.except_osv(('错误提示'), (' %s')%(card_lines,))

        sum = 0.00
        #列表遍历
        #[[0, False, {'note': '11', 'percentage': 90, 'line_no': 123, 'price': 10}],
        # [0, False, {'note': '1', 'percentage': 10, 'line_no': 432, 'price': 10}]]
        #
        #

        for card_line in range(len(card_lines)):
            dict_temp = card_lines[card_line][2]
            sum += dict_temp['percentage']
        #raise osv.except_osv(('错误提示'), (' %s')%(sum,))




        # if len(card_lines) == 1:
        #     dict_temp = card_lines[2]
        #     sum = dict_temp['percentage']
        # elif len(card_lines) > 1:
        #     for card_line in card_lines:
        #         #raise osv.except_osv(('错误提示'), (' %s')%(card_line,))
        #         dict_temp = card_line[2]
        #         sum += dict_temp['percentage']
        #         #sum += card_line[2]['percentage']
        #         #raise osv.except_osv(('错误提示'), (' %s')%(sum,))

        if sum != 100:
            raise osv.except_osv(('错误提示'), ('分期付款比例总和必须为100'))
        else:
            order =  super(designer_agreement, self).create(cr, uid, vals, context=context)
        return order

    """
    分期付款，比例必须总和为100
    """

    def write11(self, cr, uid, ids, vals, context = None):
        #分期付款
        card_lines = vals.get('card_line',[])
        if not card_lines:
            raise osv.except_osv(('错误提示'), ('必须添写付款信息'))
        #调试 最佳实践
        #设断点可以查看传递参数 F7

        #raise osv.except_osv(('错误提示'), (' %s')%(card_lines,))

        sum = 0.00
        #列表遍历
        #[[0, False, {'note': '11', 'percentage': 90, 'line_no': 123, 'price': 10}],
        # [0, False, {'note': '1', 'percentage': 10, 'line_no': 432, 'price': 10}]]
        #
        #
        if len(card_lines) == 1:
            dict_temp = card_lines[2]
            sum = dict_temp['percentage']
        elif len(card_lines) > 1:
            for card_line in card_lines:
                #raise osv.except_osv(('错误提示'), (' %s')%(card_line,))
                dict_temp = card_line[2]
                sum += dict_temp['percentage']
                #sum += card_line[2]['percentage']
                #raise osv.except_osv(('错误提示'), (' %s')%(sum,))

        if sum != 100:
            raise osv.except_osv(('错误提示'), ('分期付款比例总和必须为100'))
        else :
            res = super(designer_agreement, self).write(cr, uid, ids, vals, context = context)
        return res


    #人民币金额转大写程序Python版本
    #Copyright: zinges at foxmail.com
    #blog: http://zingers.iteye.com
    #感谢zinges提供了Python的版本

    def numtoCny(self,contract_amount):

        capUnit = ['万','亿','万','圆','']
        capDigit = { 2:['角','分',''], 4:['仟','佰','拾','']}
        capNum=['零','壹','贰','叁','肆','伍','陆','柒','捌','玖']
        snum = str('%019.02f') % contract_amount
        if snum.index('.')>16:
            return ''
        ret,nodeNum,subret,subChr='','','',''
        CurChr=['','']
        for i in range(5):
            j=int(i*4+math.floor(i/4))
            subret=''
            nodeNum=snum[j:j+4]
            lens=len(nodeNum)
            for k in range(lens):
                if int(nodeNum[k:])==0:
                    continue
                CurChr[k%2] = capNum[int(nodeNum[k:k+1])]
                if nodeNum[k:k+1] != '0':
                    CurChr[k%2] += capDigit[lens][k]
                if  not ((CurChr[0]==CurChr[1]) and (CurChr[0]==capNum[0])):
                    if not((CurChr[k%2] == capNum[0]) and (subret=='') and (ret=='')):
                        subret += CurChr[k%2]
            subChr = [subret,subret+capUnit[i]][subret!='']
            if not ((subChr == capNum[0]) and (ret=='')):
                ret += subChr

        return [ret,capNum[0]+capUnit[3]][ret=='']

    def onchange_contractamount(self, cr, uid, ids, contract_amount):
        if contract_amount > 0 :
            #这里需要注意 调用numtoCny   函数时 传参个数的统一，总监大人说了 重庆-mrshelly(49812643)  15:30:23
            #因为你使用了 self.numtoCny 所以,  有一个默认的 self 参数传过去了.
            big = self.numtoCny(contract_amount)
            return {'value':{'contract_amount_big': big}}
        else :
            return {}

    def _cal_contract_amount_by_offer(self, cr, uid, ids, field_name, args, context=None):
        res = {}
        #获得订单对象
        offer_obj = self.pool.get("designer.offer")
        #hetong_obj = self.browse(cr, uid, ids, context=context)

        for hetong in self.browse(cr, uid, ids, context=context):
            cr.execute(
                    "SELECT sum(subprice) FROM designer_offer_line WHERE card_id=%s ",(hetong.offer_ids.id,))
            res[hetong.id] = cr.fetchone()[0]#注意参数格式  ()

        return res
        #return {'value':{'contract_amount': res}}
    def _cal_contract_amount_big_by_offer(self, cr, uid, ids, field_name, args, context=None):
        res = {}
        #获得订单对象
        offer_obj = self.pool.get("designer.offer")
        #hetong_obj = self.browse(cr, uid, ids, context=context)

        for hetong in self.browse(cr, uid, ids, context=context):
            cr.execute(
                    "SELECT sum(subprice) FROM designer_offer_line WHERE card_id=%s ",(hetong.offer_ids.id,))
            res[hetong.id] =self.numtoCny(cr.fetchone()[0]) #注意参数格式  (,)
        return res




#readonly=True,states={'draft': [('readonly', False)]} 一旦提交就无法修改


    _columns = {
        'work_id': fields.many2one('designer.card', '所属工作卡', change_default=True, select=True, track_visibility='always'),
        'no': fields.char('合同编号', required=True,),
        'partner_id':fields.many2one('res.partner', '客户', required=True,
            change_default=True, track_visibility='always'),
        'contract_type': fields.many2one('designer.contract.type',string='合同类型', required=True),
        'offer_ids': fields.many2one('designer.offer', string='报价单', domain="[('state', '=', verify2)]" ),#合同金额跟报价单的关系  related
       # 'contract_amount': fields.float('合同金额', digits_compute=dp.get_precision('contract_amount'),required=True),
        'contract_amount': fields.function(_cal_contract_amount_by_offer,type='float',method="true", relation='designer.offer',string='合同金额',store=True,digits_compute=dp.get_precision('contract_amount')),
        'contract_amount_big': fields.function(_cal_contract_amount_big_by_offer,type='char',method="true", relation='designer.offer',string='合同金额大写',store=True),
        #'contract_amount_big': fields.char('合同金额大写', required=True),
        'project_ids': fields.many2one('designer.project', string='项目简报'),
        'card_line': fields.one2many('designer.agreement.rule.line', 'card_id', '付款方式'),
        'state': fields.selection([
            ('draft', '草稿中'),
            ('open', '已批准'),
            ('verify1', '一次确认'),
            ('verify2', '二次确认'),
            ('cancel', '已拒绝')],
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
    _rec_name = "no"

    _defaults = {
        "no":_get_seq ,
        'state': lambda *a: 'draft',

    }
    def designer_agreement_draft(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)

    def designer_agreement_cancel1(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)

    def designer_agreement_cancel2(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)

    def designer_agreement_open(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'open'}, context=context)

    def designer_agreement_verify1(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'verify1'}, context=context)

    def designer_agreement_verify2(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'verify2'}, context=context)



class designer_agreement_rule_line(osv.osv):
    """ 项目工作卡物料管理"""
    _name = 'designer.agreement.rule.line'
    _inherit = ['mail.thread']
    _columns = {
        'card_id': fields.many2one('designer.agreement', '工作卡', ondelete='cascade', select=True),
        'line_no': fields.integer('次数', required=True,change_default=True, select=True, track_visibility='always'),
        'percentage': fields.float('比例',digits_compute= dp.get_precision('Price'), required=True, change_default=True, select=True, track_visibility='always'),
        'price': fields.float('金额',digits_compute= dp.get_precision('Price'), required=True, change_default=True, select=True, track_visibility='always'),
        'note': fields.text('里程碑',size=64,change_default=True, select=True, track_visibility='always'),
    }
    _sql_constraints = [
    ]
    _rec_name = "line_no"
    _defaults = {
        'line_no': 1,
    }
    _order = 'line_no asc'

