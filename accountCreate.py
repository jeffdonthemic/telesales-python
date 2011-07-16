# accountCreate.py

import os
import beatbox

from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import RequestHandler

sfdcUsername = "YOUR-USERNAME"
sfdcPassword = "YOUR-PASSWORD-TOKEN"

class AcctCreateHandler(RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), "templates/accountCreate.html")
        self.response.out.write(template.render(path, {}))
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
        
        newAccount = {"Name": self.request.get("name"), "BillingCity": self.request.get("billingCity"), "BillingState": self.request.get("billingState"), 
                      "Phone": self.request.get("phone"),"Website": self.request.get("website"), "type": "Account"}
        create_result = self.sforce.create([newAccount])
        
        if create_result[0]["success"] == False:
            self.response.out.write( create_result[0]["errors"])
        else:
            self.response.out.write(create_result)
            self.redirect("/accountDisplay?accountId="+create_result[0]["id"])
        