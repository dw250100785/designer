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
import sys
reload(sys)
sys.setdefaultencoding('utf8')#中文乱码

import designer_card   #工作卡
import designer_project        #项目简报
import designer_brand  #品牌
import designer_idea   #创意简报
import designer_archive   #项目备档单
import designer_order   #项目工单
import designer_paper   #竟稿申请
import designer_policy   #创意策略
import designer_inquiry   #询价单
import designer_offer   #报价单
import designer_bill   #发票
import designer_agreement   #合同
import cn_auto_select_smtp  #中国化
import cn_auto_setup        #中国化   自动安装
import controllers    #one2many attachments 附件下载bug
#import res_partner





