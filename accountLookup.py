# accountLookp.py

import os
import beatbox

from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import RequestHandler

sfdcUsername = "YOUR-USERNAME"
sfdcPassword = "YOUR-PASSWORD-TOKEN"

class AcctLookupHandler(RequestHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__), "templates/accountLookup.html")
		template_values = {"accounts": [],
						   "accountName": "ACME"};
		self.response.out.write(template.render(path, template_values))
	def post(self):
		# Retrieve account name from post data
		accountName = self.request.get("accountName")
		# Attempt a login
		self.sforce = beatbox.PythonClient()
		try:
			login_result = self.sforce.login(sfdcUsername, sfdcPassword)
		except beatbox.SoapFaultError, errorInfo:
			path = os.path.join(os.path.dirname(__file__), "templates/loginFailed.html")
			self.response.out.write(template.render(path, {"errorCode": errorInfo.faultCode, 
			                                               "errorString": errorInfo.faultString}))
			return
				
		query_result = self.sforce.query("SELECT Id, Name, Phone, BillingCity, BillingState FROM Account WHERE Name LIKE '%" + accountName + "%'")
		records = query_result["records"]
		
		template_values = {"accounts": records,
						   "accountName": accountName};
		path = os.path.join(os.path.dirname(__file__), "templates/accountLookup.html")
		self.response.out.write(template.render(path, template_values))
		