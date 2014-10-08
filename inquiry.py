import time
from openerp.osv import fields, osv
from openerp import workflow
from openerp.tools.translate import _

class initial_report(osv.osv):
	_name = "report.initial"
	_description = "Initial Report Filed"
	_columns = {
		'title': fields.char('Title', size=128, required=True),
		'description': fields.text('description'),
		'against_person': fields.many2one('hr.employee', 'Accused Person'),
		'accuser': fields.many2one('hr.employee', 'Accuser Person'),
		'accuser_type': fields.selection([('branch','Branch'),('ro','RO'),('audit','Audit'),('vigilance','Vigilance'),('cbi', 'CBI')], 'Report From', readonly=True, select=True),
		'report_id': fields.char('Report Number', size=128, required=True),
		'showcause': fields.many2one('showcause', 'Show Cause Notice'),
	}
initial_report()

class iac_recommendation(osv.osv):
	_name = "iac.recommendation"
	_description = "Details about the IAC Comitte"
	_columns = {
		'showcause_memo': fields.many2one('showcause', 'Showcause'),
		'gm': fields.many2one('hr.employee', 'GM'),
		'meeting_date': fields.datetime('Meeting Date'),
		'meeting_detail': fields.html('Meeting Summary'),
		'date': fields.datetime('Date'),
	}

iac_recommendation()

class cvo_recommendation(osv.osv):
	_name = "cvo.recommendation"
	_description = "CVO Recommendations"
	_columns = {
		'cvo': fields.many2one('hr.employee','CVO'),
		'cvo_feedback': fields.html('CVO Feedback'),
		'date': fields.datetime('Date'),
		'cvc_needed': fields.boolean('CVC Needed'),
	
	
	}
cvo_recommendation()

class cvc_advice(osv.osv):
	_name = "cvc.advice"
	_description = "CVC Advice"
	_columns = {
		'sugested_officer': fields.many2one('hr.employee',"Sugested Officer "),
		'designation' : fields.char('Designation'),
		'allegation_brief' : fields.text('Allegation In Brief'),
		'defence' : fields.char('Defense'),
		'views_da' : fields.text("View and Comments of DA"),
		'views_cvo' : fields.text('Views of CVO'),
		'date': fields.datetime('Date'),
	}
cvc_advice()

class disciplinary_authority(osv.osv):
	_name = 'disciplinary.authority'
	_columns = {
		'authority_name' : fields.many2one('hr.employee','Authorize Person'),
		'designation': fields.char('Designation'),
		'date': fields.datetime('Date'),
		'remark' : fields.text('Remark'),
		'decision' : fields.selection([('minorpenalty','Minor Penalty'),('majorpenalty','Major Penalty')],'Decision'), 
	}
disciplinary_authority()

class show_cause(osv.osv):
	_name = "showcause"
	_inherit = ['iac.recommendation','cvo.recommendation','cvc.advice','disciplinary.authority']
	_description = "Show Cause Memorandum"

	def showcause_step1(self, cr, uid, ids, context=None):
		self.write(cr, uid, ids, {'state' : 'step2'}, context=context)
		return True

	def showcause_step2(self, cr, uid, ids, context=None):
		self.write(cr, uid, ids, {'state' : 'step3'}, context=context)
		return True

	def showcause_step3(self, cr, uid, ids, context=None):
		self.write(cr, uid, ids, {'state' : 'step4'}, context=context)
		return True

	def showcause_step4(self, cr, uid, ids, context=None):
		self.write(cr, uid, ids, {'state' : 'step5'}, context=context)
		return True

	def showcause_step5(self, cr, uid, ids, context=None):
		cvc_needed = self.read(cr,uid,ids,{'cvc_needed'},context=context)
		print "Gaurav Sahu"
		print cvc_needed[0]['cvc_needed']
		if cvc_needed[0]['cvc_needed'] == True:
			print "Inside IF"
			self.write(cr, uid, ids, {'state' : 'step6'}, context=context)
			return True
		else:
			print "Inside Else"
			self.write(cr, uid, ids, {'state' : 'step7'}, context=context)
			return True

	def showcause_step6(self, cr, uid, ids, context=None):
		self.write(cr, uid, ids, {'state' : 'step7'}, context=context)
		return True

	def showcause_step7(self, cr, uid, ids, context=None):
		decision = self.read(cr,uid,ids,{'decision'}, context=context),
		print "Gaurav Sahu"
		print decision[0][0]['decision']
		if decision[0][0]['decision'] == "minorpenalty": 
			self.write(cr, uid, ids, {'state' : 'step8'}, context=context)
			return True
		else:
			self.write(cr, uid, ids, {'state' : 'step9'}, context=context)
			return True
		
	_columns = {
		'rohead_comments_line':fields.one2many('showcause.charge','showcause'),
		'gm_line': fields.one2many('iac.recommendation' , 'showcause'),
		'title': fields.char('Title', size=128, required=True),
		'description': fields.text('Description'),
		'against_person': fields.many2one('hr.employee', 'Accused'),
		'issued_by': fields.many2one('hr.employee', 'Issued By'),
		'report': fields.many2one('report.initial','Report'),
		'issued_on': fields.datetime('Issued on', size=64),
		'acusee_reply': fields.many2one('acusee.reply','Acusee Reply'),
		'rohead_comments': fields.many2one('rohead.comments','RO Head Comments'),
		'charges': fields.one2many('showcause.charge','showcause'),
		'vigilance_status': fields.selection([('vigilance','Vigilance'), ('nonvigilance','Non Vigilance')],'Vigilance Case'),
		'state' : fields.selection([
			('step1', 'Showcause'),
			('step2', 'Reply'),
			('step3', 'RO Comments'),
			('step4', 'IAC'),
			('step5', 'CVO'),
			('step6', 'CVC'),
			('step7','DA Penalty'),
			('step8','Ist Stage Advice'),
			('step9', 'Article Of Charge'),],"State"),
	}
	_defaults = {
		'state': 'step1'
	}
	def onchange_iac_vigilance_status(self, cr, uid, ids, vigilance_status, context=None):
		self.write(cr, uid, ids, {'vigilance_status' : vigilance_status}, context=context)
			
			
	
show_cause()

class charges_showcause(osv.osv):
	_name = "showcause.charge"
	_description = "The charges associated with Showcause"
	_columns = {
		'allegation_id': fields.integer('Allegation Id'),
		'allegation': fields.text('Allegation', size=512),
		'explanation': fields.text('Explanations', size=512),
		'rohead_comments': fields.text('RO Head Comments', size=512),
		'showcause': fields.many2one('showcause', 'Showcause'),
	}
charges_showcause()


class accusee_reply(osv.osv):
	_name = "acusee.reply"
	_description = "The replies of the Acusee"
	_columns = {
		'title': fields.char('Title', size=128),
		'description': fields.html('Description'),
		'showcause': fields.many2one('showcause', readonly=True),
		'time': fields.datetime('time', size=64),
	}
accusee_reply()

class rohead_comments(osv.osv):
	_name = "rohead.comments"
	_description = "Comments of RO Head"
	_columns = {
		'title': fields.char('title', size=128),
		'comments': fields.text('Comments of Regional Head'),
		'showcause': fields.many2one('showcause', readonly=True),
		'time': fields.datetime('time', size=64),
	}
rohead_comments()

class cso_recommendation(osv.osv):
	_name = "cso.recommendation"
	_columns = {
		'officer_name' : fields.many2one("hr.employee","Officer Name"),
		'designation':fields.char('Designation'),
		'department' : fields.many2one("hr.department",'Department'),
		'defence_statement' : fields.text("Defense Statement"),
 	}
cso_recommendation()

class ia_inquiry(osv.osv):
	_name = "ia.inquiry"
	_columns = {
		'ia_comments' : fields.text("IA Comments"),
		'upload_data' : fields.binary('Upload Data'),
	}
ia_inquiry()

class charge_sheet(osv.osv):
	_name = "charge.sheet"
	_inherit = ['cso.recommendation','ia.inquiry']

	def charge_step1(self, cr, uid, ids, context=None):
		self.write(cr, uid, ids, {'state' : 'step2'}, context=context)
		return True

	def charge_step2(self, cr, uid, ids, context=None):
		self.write(cr, uid, ids, {'state' : 'step3'}, context=context)
		return True

	def charge_step3(self, cr, uid, ids, context=None):
		self.write(cr, uid, ids, {'state' : 'step4'}, context=context)
		return True
		
	def charge_step(self, cr, uid, context=None):
		sheet_id = 14
		charge_sheet_obj = self.pool.get('charge.sheet').browse(cr, uid, sheet_id)
		create_date = charge_sheet_obj.create_date
		self.write(cr, uid, [14], {'state' : 'step4'}, context=context)
		return True

	def charge_step4(self, cr, uid, ids, context=None):
		self.write(cr, uid, ids, {'state' : 'step5'}, context=context)
		return True

	def charge_step5(self, cr, uid, ids, context=None):
		self.write(cr, uid, ids, {'state' : 'step6'}, context=context)
		return True

	def charge_step6(self, cr, uid, ids, context=None):
		self.write(cr, uid, ids, {'state' : 'step7'}, context=context)
		return True
	
	def charge_step7(self, cr, uid, ids, context=None):
		self.write(cr, uid, ids, {'state' : 'step8'}, context=context)
		return True

	def charge_step8(self, cr, uid, ids, context=None):
		self.write(cr, uid, ids, {'state' : 'step9'}, context=context)
		return True

	_columns = {
		"showcause_id" : fields.many2one('showcause',"Showcause"),
		'title' : fields:.char('Title'),
		"witness_name" : fields.many2one('hr.employee',"Witness Name"),
		"first_advice" : fields.text('First Stage Advice',readonly=True),
		'vigilance_status': fields.char('Vigilance Status',readonly=True),
		'inquiry' : fields.boolean('Inquiry Status'),
		'start_date' : fields.datetime('Date'),
		'da_comments' : fields.text("Da Comments"),
		'cso_comments' : fields.text("CSO Submission"),
		'da_penality_text' : fields.text('DA Penalty Text'),
		'concure_ia' : fields.boolean('Concure with IA'),
		'cvo_feedback' : fields.text("CVO Feedback"),
		'final_penality_order' : fields.html('Final Penalty Order'),
		'state' : fields.selection([
			('step1', 'Draft'),
			('step2', 'Waiting For Vigilance'),
			('step3', 'Charge Sheet Filed'),
			('step4', 'Inquiry'),
			('step5', 'DA Finding '),
			('step6', 'CSO Submission'),
			('step7', 'DA Penalty'),
			('step8', 'CVO Advice'),
			('step9','Penalty Order')],"State"),
	}
	_defaults = {
		'state': 'step1'
	}
	def onchange_showcause_id(self, cr, uid, ids, showcause_id, context=None):
		value = {'first_advice': False,'vigilance_status':False}
		if showcause_id:
			showcause_obj = self.pool.get('showcause').browse(cr, uid, showcause_id)
			value['first_advice'] = showcause_obj.decision
			value['vigilance_status'] = showcause_obj.vigilance_status
			return {'value': value}
charge_sheet()
