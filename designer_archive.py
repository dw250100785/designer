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

class designer_archive(osv.osv):
    """ 项目备档单"""
    _name = 'designer.archive'
    _description = "designer_archive"
    #多继承会导致 tree  view 无法加载数据
    #对于 ir.attachment模块尽量使用  关系引用来实现！！！


    def _get_seq(self, cr, uid, ids, context=None):
        return self.pool.get('ir.sequence').get(cr, uid, 'designer.archive')


    _inherit = ['mail.thread']
    _columns = {
        'work_id': fields.many2one('designer.card', '所属工作卡', change_default=True, select=True, track_visibility='always'),
        'archive_no': fields.char('编号', required=True),
        'word_line': fields.one2many('designer.archive.word.line', 'word_id', '文字'),
        'image_line': fields.one2many('designer.archive.image.line', 'image_id', '图片'),
        'sample_line': fields.one2many('designer.archive.sample.line', 'sample_id', '样稿'),
        'finished_line': fields.one2many('designer.archive.finished.line', 'finished_id', '成品'),
        'product_line': fields.one2many('designer.archive.product.line', 'product_id', '实物照片'),
        'project_id': fields.many2one('designer.project', string='项目简报'),
        'partner_id':fields.related(
            'project_id',#关联字段
            'partner_id',#项目简报的
            string='客户',
            type='many2one',
            relation='res.partner',
            readonly=True,
            store=True
        ),
        'state': fields.selection([('draft', '草稿中'),
            ('open', '已批准'),
            ('cancel', '已拒绝'),
            ('close', '已完成')],
            '状态', readonly=True, track_visibility='onchange',
        )
    }

    _rec_name = 'archive_no'
    _sql_constraints = [
        ('archive_no', 'unique(archive_no)', 'The name of the idea must be unique')
    ]
    _defaults = {
        'archive_no':_get_seq,
        'state': lambda *a: 'draft',
    }
    _order = 'archive_no asc'

    def designer_idea_cancel(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)

    def designer_idea_open(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'open'}, context=context)

    def designer_idea_close(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'close'}, context=context)

    def designer_idea_draft(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)


class designer_archive_word_line(osv.osv):
    """ 文字"""
    _name = 'designer.archive.word.line'
    _inherit = ['ir.attachment']
    _columns = {
        'word_id': fields.many2one('designer.archive', '工作卡', ondelete='cascade', select=True),
        'name': fields.char('文件', size=64, required=True),
        'line_no': fields.char('编号', required=True,change_default=True, select=True, track_visibility='always'),
        'position': fields.char('位置',change_default=True, select=True, track_visibility='always'),
        'note': fields.text('备注',size=64,change_default=True, select=True, track_visibility='always'),
    }
    _sql_constraints = [
       # ('line_no', 'unique(line_no)', 'The name of the idea must be unique')
    ]
    _defaults = {
    }
    _order = 'line_no asc'

class designer_archive_image_line(osv.osv):
    """ 图片"""
    _name = 'designer.archive.image.line'
    _inherit = ['ir.attachment']
    _columns = {
        'image_id': fields.many2one('designer.archive', '工作卡', ondelete='cascade', select=True),
        'name': fields.char('文件', size=64, required=True),
        'line_no': fields.char('编号', required=True,change_default=True, select=True, track_visibility='always'),
        'position': fields.char('位置',change_default=True, select=True, track_visibility='always'),
        'note': fields.text('备注',size=64,change_default=True, select=True, track_visibility='always'),
    }
    _sql_constraints = [
      #  ('line_no', 'unique(line_no)', 'The name of the idea must be unique')
    ]
    _defaults = {
    }
    _order = 'line_no asc'

class designer_archive_sample_line(osv.osv):
    """ 样稿"""
    _name = 'designer.archive.sample.line'
    _inherit = ['ir.attachment']
    _columns = {
        'sample_id': fields.many2one('designer.archive', '工作卡', ondelete='cascade', select=True),
        'name': fields.char('文件', size=64, required=True),
        'line_no': fields.char('编号', required=True,change_default=True, select=True, track_visibility='always'),
        'position': fields.char('位置', change_default=True, select=True, track_visibility='always'),
        'note': fields.text('备注',size=64,change_default=True, select=True, track_visibility='always'),
    }
    _sql_constraints = [
       # ('line_no', 'unique(line_no)', 'The name of the idea must be unique')
    ]
    _defaults = {
    }
    _order = 'line_no asc'

class designer_archive_finished_line(osv.osv):
    """ 成品"""
    _name = 'designer.archive.finished.line'
    _inherit = ['ir.attachment']
    _columns = {
        'finished_id': fields.many2one('designer.archive', '工作卡', ondelete='cascade', select=True),
        'name': fields.char('文件', size=64, required=True),
        'line_no': fields.char('编号', required=True,change_default=True, select=True, track_visibility='always'),
        'position': fields.char('位置',change_default=True, select=True, track_visibility='always'),
        'note': fields.text('备注',size=64,change_default=True, select=True, track_visibility='always'),
    }
    _sql_constraints = [
       # ('line_no', 'unique(line_no)', 'The name of the idea must be unique')
    ]
    _defaults = {
    }
    _order = 'line_no asc'

class designer_archive_product_line(osv.osv):
    """ 实物照片"""
    _name = 'designer.archive.product.line'
    _inherit = ['ir.attachment']
    _columns = {
        'product_id': fields.many2one('designer.archive', '工作卡', ondelete='cascade', select=True),
        'line_no': fields.char('编号', required=True,change_default=True, select=True, track_visibility='always'),
        'name': fields.char('文件', size=64, required=True),
        'note': fields.text('备注',size=64,change_default=True, select=True, track_visibility='always'),
    }
    _sql_constraints = [
      #  ('line_no', 'unique(line_no)', 'The name of the idea must be unique')
    ]
    _defaults = {
    }
    _order = 'line_no asc'

