from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db

import contest
from contest import Contest
import datetime
import contest
import time
import common
import calendar
import pytz
import logging
import os
import cgi

class ContestEditor(webapp.RequestHandler):

    def get(self):
        # default values for template parameters
        default_time = datetime.datetime.now()
        default_time_zone = pytz.timezone('UTC')
        default_contest_type = "Training"

        # initalizing contest
        cont = None
        cont_id = self.request.get("id")
        if cont_id:
            cont = contest.get_contest_by_id(cont_id)
            if not cont:
                self.redirect('error?message=No+contest+for+given+id') # it means that contest is lost in data store or somebody tries to hack the system
                return

            utc = pytz.timezone('UTC')
            default_time_zone = pytz.timezone(cont.time_zone)
            default_time = default_time_zone.normalize(utc.localize(cont.date_and_time).astimezone(default_time_zone))
            default_contest_type = cont.contest_type

        # initializing templates dictionary
        template_values = {'time_zones' : pytz.common_timezones,
                           'contest' : cont,
                           'id' : cont_id,
                           'default_year' : default_time.year,
                           'default_month' : default_time.month - 1,
                           'default_day' : default_time.day,
                           'default_time' : default_time.strftime("%H:%M"),
                           'default_time_zone' : default_time_zone,
                           'default_contest_type' : default_contest_type}

        # writing response
        self.response.out.write(template.render(os.path.join('templates', 'edit_contest.html'), 
                                                template_values,
                                                common.DEBUG))

    def post(self):
        contest_dict = contest.get_contest_dict_from_request(self.request)
        parsed_time = time.strptime(contest_dict['time'], "%H:%M")
        date_and_time = datetime.datetime(year = int(contest_dict["year"]),
                                          month = list(calendar.month_name).index(contest_dict["month"]),
                                          day = int(contest_dict["day"]),
                                          hour = parsed_time.tm_hour,
                                          minute = parsed_time.tm_min)
        timezone = pytz.timezone(contest_dict["time_zone"])
        date_and_time = timezone.localize(date_and_time)
        contest_dict["date_and_time"] = date_and_time

        contest_dict["full_name"] = contest_dict["full_name"].replace('\n', ' ')

        cont = None
        contest_id = self.request.get("id")
        if contest_id:

            cont = contest.get_contest_by_id(contest_id)
            for prop in cont.properties():
                setattr(cont, prop, contest_dict[prop])
            if not cont:
                self.redirect('\error?message=No contest with given id')
                return
        else:
            contest_dict["full_name"] = cgi.escape(contest_dict["full_name"])
            contest_dict["short_name"] = cgi.escape(contest_dict["short_name"])
            contest_dict["info"] = cgi.escape(contest_dict["info"])
            cont = Contest(parent = contest.PARENT_KEY, **contest_dict)

        cont.put()

        self.redirect('/')
        
class ContestDeletor(webapp.RequestHandler):
    def get(self):
        cont_id = self.request.get("id")
        if not cont_id:
            self.redirect('\error?message=Need an id to delete contest')
            return
        cont = contest.get_contest_by_id(cont_id)
        if not cont:
            self.redirect('\error?message=No contest with given id')
            return
        cont.delete()

        self.redirect('/')
        

def main():
    application = webapp.WSGIApplication([('/edit_contest*', ContestEditor),
                                          ('/delete_contest*', ContestDeletor)],
                                         debug = common.DEBUG)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()                                              


    