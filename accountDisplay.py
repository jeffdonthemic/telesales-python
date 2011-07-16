# accountDisplay.py

import os
import beatbox

from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import RequestHandler 

sfdcUsername = "YOUR-USERNAME"
sfdcPassword = "YOUR-PASSWORD-TOKEN"

class AcctDisplayHandler(RequestHandler):
    def get(self):
        # Retrieve account name from post data
        accountId = self.request.get("accountId")
        # Attempt a login
        self.sforce = beatbox.PythonClient()
        try:
            login_result = self.sforce.login(sfdcUsername, sfdcPassword)
        except beatbox.SoapFaultError, errorInfo:
            path = os.path.join(os.path.dirname(__file__), "templates/loginFailed.html")
            self.response.out.write(template.render(path, {"errorCode": errorInfo.faultCode, 
                                                           "errorString": errorInfo.faultString}))
            return
                
        #fetch the account
        retreive_results = self.sforce.retrieve( 'Id, Name, Phone, BillingCity, BillingState, Website','Account', accountId )
        #fetch all of its opportunities
        query_result = self.sforce.query("Select id, name, stagename, amount, closeDate, probability, ordernumber__c from Opportunity where AccountId = '"+accountId+"'")
        opportunities = query_result["records"]
        opportunityCount = query_result["size"]
        
        # Render the output
        template_values = {"account": retreive_results[0],
                           "opportunities": opportunities,
                           "opportunityCount": opportunityCount};
        path = os.path.join(os.path.dirname(__file__), "templates/accountDisplay.html")
        self.response.out.write(template.render(path, template_values))