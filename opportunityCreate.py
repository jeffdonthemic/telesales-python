# accountCreate.py

import os
import beatbox

from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import RequestHandler

sfdcUsername = "YOUR-USERNAME"
sfdcPassword = "YOUR-PASSWORD-TOKEN"

class OppCreateHandler(RequestHandler):
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
        retreive_results = self.sforce.retrieve( 'Name,Id','Account', accountId )
        
        path = os.path.join(os.path.dirname(__file__), "templates/opportunityCreate.html")
        template_values = {"accountId": accountId,
                           "accountName": retreive_results[0]["Name"]};
        self.response.out.write(template.render(path, template_values))
        
    def post(self):
        
        # Attempt a login
        self.sforce = beatbox.PythonClient()
        try:
            login_result = self.sforce.login(sfdcUsername, sfdcPassword)
        except beatbox.SoapFaultError, errorInfo:
            path = os.path.join(os.path.dirname(__file__), 'templates/simple_login_failed.html')
            self.response.out.write(template.render(path, {'errorCode': errorInfo.faultCode, 
                                                           'errorString': errorInfo.faultString}))
            return
        
        newOpp = {"Name": self.request.get("name"), "AccountId": self.request.get("accountId"), "Amount": self.request.get("amount"), 
                  "StageName": self.request.get("stageName"), "Probability": self.request.get("probability"), "CloseDate": self.request.get("closeDate"), 
                  "OrderNumber__c": self.request.get("orderNumber"), "type": "Opportunity"}
        create_result = self.sforce.create([newOpp])
        
        if create_result[0]["success"] == False:
            self.response.out.write( create_result[0]["errors"])
        else:
            self.response.out.write(create_result)
            self.redirect("/accountDisplay?accountId="+self.request.get("accountId"))
        