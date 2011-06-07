from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

import common
import os

class ErrorDisplayer(webapp.RequestHandler):
    def get(self):
        message = self.request.get("message")
        self.response.out.write("The following error occured: %s" % message)

class AboutDisplayer(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render(os.path.join("templates", "about.html"), {}, common.DEBUG))

def main():
    application = webapp.WSGIApplication([('/error*', ErrorDisplayer),
                                          ('/about*', AboutDisplayer)],
                                         debug = common.DEBUG)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()                                              
