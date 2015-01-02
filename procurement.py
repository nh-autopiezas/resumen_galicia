from openerp.osv import osv,fields


class procurement_order(osv.osv):
	_name = "procurement.order"
	_inherit = "procurement.order"
	
	def procurement_order_run(self,cr,uid,context=None):

		import pdb;pdb.set_trace()
	        procurement_obj = self.pool.get('procurement.order')
	        procurement_ids = procurement_obj.search(cr, uid, [('state', '=', 'exception')])
		for procurement_id in procurement_ids:
			return_id = procurement_obj.run(cr,uid,procurement_id)
			print return_id
			print procurement_id

		return True

	def procurement_order_cancel(self,cr,uid,context=None):

		import pdb;pdb.set_trace()
	        procurement_obj = self.pool.get('procurement.order')
	        procurement_ids = procurement_obj.search(cr, uid, [('state', '=', 'exception')])
		for procurement_id in procurement_ids:
			return_id = procurement_obj.cancel(cr,uid,procurement_id)
			print return_id
			print procurement_id

	
procurement_order()
