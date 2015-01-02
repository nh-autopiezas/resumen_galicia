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

from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import date
from datetime import datetime
from openerp import netsvc
import base64


class resumen_galicia_import(osv.osv_memory):
    _name = 'resumen.galicia.import'
    _description = 'Importa extracto bancario Galicia'

    _columns = {
        # 'filename_po': fields.char('Filename', required=True),
	'filename_resumen': fields.binary(string='Archivo'),
        'first_row_column': fields.boolean('1st Row Column Names'),
    }

    _defaults = {
	'first_row_column': True,
	}

    def resumen_galicia_import(self, cr, uid, ids, context=None):

	res = self.read(cr,uid,ids,['filename_resumen','statement_id','journal_id'])
	filename_resumen = res[0]['filename_resumen']
	res_first_row = self.read(cr,uid,ids,['first_row_column'])
	first_row = res_first_row[0]['first_row_column']

	if not filename_resumen:
		raise osv.except_osv(_('Error!'), _("Debe ingresar un archivo a importar!!!"))
		return {'type': 'ir.actions.act_window_close'}

	file=base64.decodestring(filename_resumen)
	lines=file.split('\n')

        statement_ids = context['active_ids']
	if not statement_ids:
		return None
	statement = self.pool.get('account.bank.statement').browse(cr,uid,statement_ids)

	index = 1
	for line in lines:
		if ((index > 1 and first_row) or (index > 0 and not first_row)):
			# cadena = line.split('\t')
			cadena = line.split(';')
			slist = cadena[0].split('/')
			if len(slist) == 3:
				try:
					sdate = date(int(slist[2]),int(slist[1]),int(slist[0]))
				except:
					# No contiene una fecha, es posible que no sea una linea con movimientos
					continue 
				vals_statement_line = {
					'date': str(sdate),
					'name': cadena[1],
					'ref': cadena[2],
					'journal_id': statement.journal_id.id,
					}
				cadena[3] = cadena[3].replace(',','.')
				cadena[4] = cadena[4].replace(',','.')
				amount = float(cadena[3])
				if amount > 0:
					amount = amount * (-1)
				else:
					amount = float(cadena[4])
				vals_statement_line['amount'] = amount
				vals_statement_line['statement_id'] = statement.id
				return_id = self.pool.get('account.bank.statement.line').create(cr,uid,vals_statement_line)
					
		index += 1		
        return {}

resumen_galicia_import()
