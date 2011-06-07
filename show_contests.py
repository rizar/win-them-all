from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db

import common
import os   
import pytz
import time
import contest
import logging
import datetime
from contest import Contest

class ContestsShow(webapp.RequestHandler):
    def get(self):
        # initialize request time boundaries
        after_utc = self.request.get("after_utc")
        before_utc = self.request.get("before_utc")
        
        after_time = None
        if after_utc:
            after_time = int(after_utc) // 1000
        else:
            after_time = time.time()
            after_utc = int(after_time * 1000)

        before_time = None
        if before_utc:
            before_time = int(before_utc) // 1000
        else:
            before_time = time.time() + 86400 * 28
            before_utc = int(before_time * 1000)

        # make the database query
        query = Contest.all().ancestor(contest.PARENT_KEY)
        contests = list(query.filter("date_and_time >= ", 
                                     datetime.datetime.fromtimestamp(after_time))
                             .filter("date_and_time <= ", 
                                     datetime.datetime.fromtimestamp(before_time))
                             .order("date_and_time"))

        #make list of boxes containing contest and it's UTC timestamp
        boxes = [contest.Box(cont) for cont in contests]
        self.response.out.write(template.render(os.path.join("templates", "show_contests.html"), 
                                                {"boxes" : boxes,
                                                "after_utc" : after_utc,
                                                "before_utc" : before_utc},
                                                common.DEBUG))

        """unix_times = list()
        orig_times = list()
        ids = list()

        utc = pytz.timezone('UTC')
        for cont in contests:
            cont_time_zone = pytz.timezone(cont.time_zone)
            date_and_time = cont_time_zone.normalize(utc.localize(cont.date_and_time).astimezone(cont_time_zone))
            orig_times.append(date_and_time)
            unix_times.append(int(time.mktime(date_and_time.astimezone(utc).timetuple())))
            ids.append(cont.key().id())

        self.response.out.write(template.render(os.path.join('templates', "show_contests.html"),
                                               {"data" : zip(contests, orig_times, unix_times, ids),
                                                },
                                               debug = common.DEBUG))"""

class DetailsShow(webapp.RequestHandler):
    def get(self):
        # initalizing contest
        cont = None
        cont_id = self.request.get("id")
        if cont_id:
            cont = contest.get_contest_by_id(cont_id)
            if not cont:
                self.redirect('/error?message=No+contest+for+given+id') # it means that contest is lost in data store or somebody tries to hack the system
                return
        else:
            logging.info("redirection to error...")
            self.redirect('/error?message=Need+id')                                            
            return


        self.response.out.write(template.render(os.path.join("templates", "contest_details.html"),
                                                             {"box" : contest.Box(cont)},
                                                             common.DEBUG))

def main():
    application = webapp.WSGIApplication([('/', ContestsShow),
                                          ('/contest_details*', DetailsShow)],
                                         debug = common.DEBUG)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()                                              
