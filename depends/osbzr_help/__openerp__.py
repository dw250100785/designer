#-*- encoding: utf-8 -*-
# __author__ = jeff@osbzr.com
##############################################################################
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

{
    "name" : "Get help from osbzr",
    "version" : "1.0",
    "description" : '''
    We put a new blue help button  on each page 
	when you are confused by current form 
	or don't know what this module provide 
	click it 
	then waiting for a surprise 
    ''',
    "author" : "jeff@osbzr.com",
    "website" : "http://www.osbzr.com",
    "depends" : ['base'],
    "data" : ['osbzr_help_view.xml'],
    "installable" : True,
    "web": True,
    "js":["static/src/js/osbzr_help.js"],
    "css":["static/src/css/osbzr_help.css"],
    "qweb":[
        "static/src/xml/*.xml",
    ],
    "images":['static/src/img/logo.jpg'],
    "certificate" : "",
    "category":'Generic Modules/Others'
}
