#-*- ecoding: utf-8 -*-
# __author__ = jeff@osbzr.com

from osv import fields, osv

class osbzr_help(osv.osv):
    '''
	Add help on each module
	'''
    _inherit= 'ir.module.module'
    def open_osbzr_help(self, cr, uid, ids, context=None):
        return {
            'type':'ir.actions.act_url',
            'url':'http://www.osbzr.com/help.php?page='+self.browse(cr, uid, ids, context)[0].name or '',
            'target':'new',
        }
osbzr_help()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

