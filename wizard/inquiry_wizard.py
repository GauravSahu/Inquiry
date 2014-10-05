from openerp.osv import fields, osv

class  allegee_reply_wizard(osv.osv_memory):
	_name = 'allegee.reply'
	_description = 'Allegee Reply'
	_columns = {
		'subject': fields.char('Subject'),
		'reply_comment': fields.text("Reply Comment"),
	}
allegee_reply_wizard()

class rocomment_ittreter(osv.osv_memory):
	_name = 'rocomment.ittreter'
	_columns = {
		'id' : fields.integer('Id'),
	}
	_default = {
		'id' : 1
	}
rocomment_ittreter()

class rohead_comment_wizard(osv.osv_memory):
	_name = "rohead.comment"
	_columns = {
		
		'allegation': fields.char('Allegation', size=512, required=True),
		'explanation': fields.char('Explanations', size=512, required=True),
		'rohead_comments': fields.char('RO Head Comments', size=512, required=True),
	}
	_default={
		'allegation' : lambda self,cr,uid,context={}: self.pool.get('showcause.charge').get(cr, uid, 'allegation'),
	}
	def action_clear(self,cr,uid,ids,context=None):
		value = {'allegation': False}
		value['allegation'] = ''
		return {'value': value}


	def action_next(self, cr, uid, ids, context=None):

		return {
            'name' : 'RO Comments',
            'type': 'ir.actions.act_window',
            'res_model': 'rohead.comment',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': 'view_rohead_comment_wizard',
            'views': [(False, 'form')],
            'target': 'new',
      	}
   
rohead_comment_wizard()


class print_documents(osv.osv_memory):
	_name = 'print.documents'
	_description = "documents"
	def print_quotation(self, cr, uid, ids, context=None):
		return self.pool['report'].get_action(cr, uid, ids, 'extension_management.report_farmer', context=context)
print_documents()



