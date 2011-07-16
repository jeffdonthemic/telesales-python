# main.py

from google.appengine.ext import webapp
from google.appengine.ext.webapp import RequestHandler
from google.appengine.ext.webapp.util import run_wsgi_app
from accountLookup import AcctLookupHandler
from accountDisplay import AcctDisplayHandler
from accountCreate import AcctCreateHandler
from opportunityCreate import OppCreateHandler
	
application = webapp.WSGIApplication([("/", AcctLookupHandler),
                                      ("/accountLookup", AcctLookupHandler),
                                      ("/accountDisplay", AcctDisplayHandler),
                                      ("/accountCreate",AcctCreateHandler),
                                      ("/opportunityCreate",OppCreateHandler)
                                      ],
                                      debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()