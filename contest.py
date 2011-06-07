import pytz
import time
import datetime
import urllib

from google.appengine.ext import db

from validator import Validator

MAX_SHORT_NAME_LENGTH = 30
MAX_FULL_NAME_LENGTH = 200
MAX_INFO_LENGTH = 1000

CONTEST_TYPES = ["Training", "Competition", "Championship"]

PARENT_KEY = db.Key.from_path("ContestSet", "default_contest_set")

"""A model for contest"""
class Contest(db.Model):
    """Contest full name, for example 'TopCoder Single Round Match 500', no more than 200 symbols"""
    full_name = db.StringProperty(required = True, validator = Validator(lambda x : 0 <= len(x) <= MAX_FULL_NAME_LENGTH))
    """Contest short name, for example 'TC SRM 500', no more then 30 symbols"""
    short_name = db.StringProperty(required = True, validator = Validator(lambda x : 0 <= len(x) <= MAX_SHORT_NAME_LENGTH))
    """Date and time when contest will be held, localized to contest home timezone"""
    date_and_time = db.DateTimeProperty(required = True, validator = Validator(lambda x : 1970 <= x.year <= 2100))
    """Timezone for date_and_time"""
    time_zone = db.StringProperty(required = True, choices = map(lambda x : str(x), pytz.common_timezones))
    """Contest type"""
    contest_type = db.StringProperty(choices = CONTEST_TYPES)
    """URL to the contest home page"""
    home_page = db.LinkProperty(required = True, validator = Validator(lambda x : x.find('.') >= 0))
    """Information about the contest"""
    info = db.TextProperty(validator = Validator(lambda x : len(x) <= MAX_INFO_LENGTH))

def get_contest_by_id(contest_id):
    try:
        contest_key = db.Key.from_path("Contest", int(contest_id), parent = PARENT_KEY) 
        query = Contest.all().ancestor(PARENT_KEY).filter("__key__ = ", contest_key)
        return query.fetch(1)[0]
    except (db.BadValueError, ValueError, IndexError): # it means that contest is lost in data store or somebody tries to hack the system
       return None

def get_contest_dict_from_request(req):
    return dict([(key, req.get(key)) for key in ["full_name", "short_name", "home_page", "contest_type", "year", "month", "day", "time", "time_zone", "info"]])

class Box:
    def __init__(self, cont):
        self.contest = cont

        tz = pytz.timezone(cont.time_zone)
        utc = pytz.timezone('UTC')
        self.original_time = tz.normalize(utc.localize(cont.date_and_time).astimezone(tz)).strftime("%a %b %d %Y %H:%M:%S %Z%z ")

        self.timestamp = 1000 * int(time.mktime(cont.date_and_time.timetuple()))
    