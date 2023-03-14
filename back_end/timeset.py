from time import time
from data_sql import dm
import datetime
from error import *

# set, get, push


def time_set_now(time):
    # string
    # set a time for now
    #data = "2022-09-27 18:05:44"
    if "T" in time:
        time = time.replace("T", " ")
    print(time)
    data = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    dm.set_timenow(data)


def time_get_now():
    # get a time for now
    # if here is not time, return Error
    if dm.is_have_time() == False:
        raise ValueError("Time not set")
    now_time = dm.get_timenow()

    time_now = {
        'time': now_time
    }
    return time_now


"""{
      week: 1,
      day: 1,
      hour: 1,
      minute: 1,
      second: 1
  }
"""
#  datetime.timedelta
def time_push_now(timeslist):
    # time is a datetime object
    # make time push forward
    #datetime.datetime(2018, 11, 1, 0, 0)
    if dm.is_have_time() == False:
        raise ValueError("Time not set")
    time_now = dm.get_timenow()
    for a, b in timeslist.items():
        timeslist[a] = int(b)
    if 'hour' not in timeslist:
        timeslist['hour'] = 0
    if 'minute' not in timeslist:
        timeslist['minute'] = 0
    if 'second' not in timeslist:
        timeslist['second'] = 0
    out = time_now + datetime.timedelta(days=timeslist['day'] + timeslist['week'] * 7,
                                        hours=timeslist['hour'], minutes=timeslist['minute'], seconds=timeslist['second'])

    dm.push_time(out)
    res = {
        'time': out
    }
    return res


def time_after_now(time_input):
    now = time_get_now()['time']
    data = datetime.datetime.strptime(time_input, '%Y-%m-%d')

    if data < now:
        raise InputError('This card has expired!')
    return True
