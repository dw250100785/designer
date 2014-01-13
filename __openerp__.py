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


{
    'name': 'Designer for Wuhan',
    'version': '0.1',
    'category': 'Project Management',
    'sequence': 300,
    'summary': '武汉设计师广告行业管理软件',
    'maintainer': '250100785@qq.com',
    'description':
"""
 武汉设计师广告行业管理软件
        系统要求：
            openerp7.0

        功能:
       * 1. 集成中文报表打印
       * 2. 自动初始化中国特色设置，时间，货币，时区
       * 3. 导入淘宝产品, 同步库存
       * 4. 导入淘宝用户
       * 5. 自动评价，中差评预警
       * 6. 跟踪淘宝订单物流信息, 签收提醒
       * 7. OpenERP 的PDF报表打印下载功能，改为直接在浏览器中预览打印

        注意事项
       * 1.安装成功后，代码包中不应该有project_long_term，发现卸载它时竟然也同时卸载了designer
       * 2.怎么禁止卸载 designer
""",
    'author': 'Evebit',
    'website': 'http://evebit.com',
    'depends': [
        'web',
        'base',
        'base_setup',
        'mail',
        'project',                  #项目任务管理 项目阶段，文档，讨论
        'document',                 #文档管理
        'audittrail',               #使用审核跟踪
        ],
    'data': [
        'security/designer_security.xml',                       #权限组

        #bugs cannot read  partner
        #'security/designer_rule.xml',                           #访问规则
        'security/access_designer_base/ir.model.access.csv',    #通用组权限
        'security/access_workflow_log/ir.model.access.csv',     #工作流审批记录
        'security/access_agreement/ir.model.access.csv',
        'security/access_archive/ir.model.access.csv',
        'security/access_bill/ir.model.access.csv',
        'security/access_idea/ir.model.access.csv',
        'security/access_inquiry/ir.model.access.csv',
        'security/access_offer/ir.model.access.csv',
        'security/access_order/ir.model.access.csv',
        'security/access_paper/ir.model.access.csv',
        'security/access_policy/ir.model.access.csv',
        'security/access_project/ir.model.access.csv',
        'security/access_kehu_ae/ir.model.access.csv',#针对客户部AE
        'security/access_card/ir.model.access.csv',
        'cn_auto_setup.xml', #中国化
        "oecn_font_installer.xml",#中文报表打印
        "res_config_view.xml",#中文报表打印
        'designer_user.xml',
        'base_menu.xml',
        'audittrail_log.xml',#审核跟踪
        'designer_card_view.xml',#工作卡，统领全局
        'designer_project_view.xml',
        'designer_brand_view.xml',
        'designer_idea_view.xml',
        'designer_archive_view.xml',
        'designer_order_view.xml',
        'designer_paper_view.xml',
        'designer_policy_view.xml',
        'designer_inquiry_view.xml',
        'designer_offer_view.xml',
        'designer_bill_view.xml',
        'designer_agreement_view.xml',
        'workflow/designer_workflow.xml',
        'workflow/designer_idea_workflow.xml',
        'workflow/designer_order_workflow.xml',
        'workflow/designer_paper_workflow.xml',
        'workflow/designer_policy_workflow.xml',
        'workflow/designer_card_workflow.xml',
        'workflow/designer_bill_workflow.xml',
        'workflow/designer_inquiry_workflow.xml',#询价单   一次
        'workflow/designer_offer_workflow.xml',#报价单     两次
        'workflow/designer_agreement_workflow.xml',#合同   两次确认
    ],
    'update_xml': [],
    'js': [
        'static/src/js/*.js' #工作流审批记录   暂时不将 workflow_info模块进行兼容！！！
        'static/src/js/web_pdf_preview.js'#报表在线预览打印
    ],
    'css': [],
    'qweb': [
        'static/src/xml/*.xml',#工作流审批记录
    ],
    'demo': [],
    'test':[],
    'application': False,
    'installable': True,
    'auto_install': False,
    'images': [],
    'web_preload': True,#报表直接预览打印
    'certificate' : '001292377792581874189',
    "license": "GPL-3",
    "active": False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
