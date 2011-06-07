from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

import common
import os
import cgi

class Message(db.Model):
  who = db.StringProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)

def get_message_dict_from_request(req):
    return dict([(key, cgi.escape(req.get(key))) for key in ["who", "content"]])

PARENT_KEY = db.Key.from_path("Guestbook", "Guestbook")

class Box:
    def __init__(self, message):
        self.message = message
        self.date = message.date.strftime("%a %b %d %Y %H:%M:%S")

class GuestbookManager(webapp.RequestHandler):

    def get(self):
        n_mess_to_show = None
        try:
            n_mess_to_show = int(self.request.get("posts_to_show"))
            if not 0 <= n_mess_to_show <= 1000:
                n_mess_to_show = 10
        except:
            n_mess_to_show = 10

        boxes = [Box(message) for message in Message.all().ancestor(PARENT_KEY).order("-date").fetch(n_mess_to_show)]

        self.response.out.write(template.render(os.path.join("templates", "guestbook.html"), 
                                                            {"boxes" : boxes,
                                                             "posts_to_show" : n_mess_to_show},
                                                            common.DEBUG))

    def post(self):
        message_dict = get_message_dict_from_request(self.request)
        message = Message(parent = PARENT_KEY, **message_dict)
        message.put()

        self.redirect("/guestbook")

        

def main():
    application = webapp.WSGIApplication([('/guestbook*', GuestbookManager)],
                                         debug = common.DEBUG)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()                                              
