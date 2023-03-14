
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from timeset import *
from user import *
from host import *
from Activity import *
from other import *
from ListActs import *
import datetime

port = 5000

url = f"http://localhost:{port}/"


def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)
CORS(APP, resources={r'/*': {'origins': '*'}})

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)


# Example
# @APP.route("/echo", methods=['GET'])
# def echo():
#     data = request.args.get('data')
#     if data == 'echo':
#    	    raise InputError(description='Cannot echo "echo"')
#     return dumps({
#         'data': data
#     })


###############################################
#                 Host                        #
###############################################


'''
json format
{
  "email": "111@163.com",
  "password": "111"
}

'''


@APP.route("/host/signup", methods=['POST'])
def http_host_signup():

    data = request.get_json()
    #data = request.args
    result = host_signup(data['email'], data['password'])

    return dumps(result)


'''
json format
{
  "email": "111@163.com",
  "password": "111"
}

'''


@APP.route("/host/login", methods=['POST'])
def http_host_login():
    data = request.get_json()

    result = host_login(data['email'], data['password'])

    return dumps(result)


'''
json format
{
  "host_id":1,
  "token": "token"
}

'''


@APP.route("/host/logout", methods=['POST'])
def http_host_logout():
    data = request.get_json()

    host_logout(int(data['host_id']), data['token'])

    return {}


'''
json format
{
  "host_id":2,
  "new_password": "aaa",
  "old_password": "111",
  "token": "OuAJMxMfiIdF0ISLlIm/BoUQKynm+VCYNCJxpJRpurryViqPsgHnQLOy2QPj1Xo8zW0TkyPcKd2craKUba+5rQ=="
}

'''


@APP.route("/host/resetpassword", methods=['POST'])
def http_host_reset_password():
    data = request.get_json()

    host_reset_password(
        int(data['host_id']), data['old_password'], data['new_password'], data['token'])

    return {}


'''
json format
{
  "email":"",
  "validation":"",
  "new_password": ""
}
'''


@APP.route("/host/forgetpassword", methods=['POST'])
def http_host_forget_password():
    data = request.get_json()

    host_forget_password(
        data['email'], data['validation'], data['new_password'])

    return {}


@APP.route("/sendemail", methods=['POST'])
def http_send_email():
    data = request.get_json()

    send_email(data['email'])

    return {}


'''
json format

{ 
  "activity":{
      "start_date": "2018-8-1T10:30",
      "end_date": "2018-8-2T11:30",
      "name":"andy",
      "description": "aaa",
      "type":"music",
      "venue_name":"aaa",
      "venue_address": "aaa",
      "all_ticket":400,
      "possible_seats": 400,
      "ticket_money": 200,
      "seat_x": 20,
      "seat_y": 20   
    },
  "host_id" : 1,
  "token": "SHvdIMoErvSFkMcv27R2utFXQ4uNsYaT7UgXXXFhf9n1TMfLNgMYih73+VUijN6j3dBjtOwUlCX4wf8JzOGlww=="
}

'''


@APP.route("/host/newactivity", methods=['POST'])
def http_host_new_activity():
    data = request.get_json()

    act = data['activity']
    start = str(data['activity']['start_date']).split('T')
    date = start[0].split('-')
    start_date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
    time = start[1].split(':')
    start_time = datetime.time(int(time[0]), int(time[1]))

    end = str(data['activity']['end_date']).split('T')
    date = end[0].split('-')
    end_date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
    time = start[1].split(':')
    end_time = datetime.time(int(time[0]), int(time[1]))

    act['start_date'] = start_date
    act['end_date'] = end_date
    act['start_time'] = start_time
    act['end_time'] = end_time
    act['all_ticket'] = int(act['all_ticket'])
    act['possible_seats'] = int(act['possible_seats'])
    act['ticket_money'] = int(act['ticket_money'])
    act['seat_x'] = int(act['seat_x'])
    act['seat_y'] = int(act['seat_y'])

    result = host_new_activity(data["host_id"], act, data['token'])

    return dumps(result)


'''
json format
{
  "host_id":1,
  "activity_id":1,
  "token": "SHvdIMoErvSFkMcv27R2utFXQ4uNsYaT7UgXXXFhf9n1TMfLNgMYih73+VUijN6j3dBjtOwUlCX4wf8JzOGlww=="
}

'''


@APP.route("/host/cancelactivity", methods=['POST'])
def http_host_cancel_activity():
    data = request.get_json()
    host_cancel_activity(int(data['host_id']), int(
        data['activity_id']), data['token'])

    return {}


'''
json format
{
  "host_id":
  "token"
}

'''


@APP.route("/host/listactivities", methods=['GET'])
def http_host_list_activities():
    data = request.args
    result = host_list_activities(int(data.get('host_id')), data.get('token'))
    return dumps(result)


'''
json format
{
  "host_id":,
  "activity_id":1,
  "message": "hhh"
  "token":
}

'''


@APP.route("/host/broadcast", methods=['POST'])
def http_host_broadcast():
    data = request.get_json()

    host_broadcast_notification(int(data['host_id']), int(
        data['activity_id']), data['message'], data['token'])

    return {}



@APP.route("/host/detail", methods=['GET'])
def http_host_detail():
    data = request.args
    result = host_detail(int(data.get('host_id')), int(
        data.get('user_id')), data.get('token'))

    return dumps(result)

###############################################
#                 User                    #
###############################################


'''
json format
{
  "email": "111@163.com",
  "password": "111",
  "name_first": "andy",
  "name_last": "wang",
  "address":"xxx",
  "bill_method": "wechat",
  "account": "lll"
}

'''


@APP.route("/user/signup", methods=['POST'])
def http_user_signup():
    data = request.get_json()

    result = user_signup(data)

    return dumps(result)


'''
json format
{
  "email": "111@163.com",
  "password": "111"
}

'''


@APP.route("/user/login", methods=['POST'])
def http_user_login():
    data = request.get_json()
    result = user_login(data['email'], data['password'])

    return dumps(result)


'''
json format
{
  "user_id":
  "token":
}

'''


@APP.route("/user/logout", methods=['POST'])
def http_user_logout():
    data = request.get_json()

    user_logout(int(data['user_id']), data['token'])

    return {}


'''
json format
{
  "user_id":1,
  "new_password": "aaa",
  "old_password": "111",
  "token":"jcc/EIZvzYiWtZMEO4F8nn1yGuBkebdp3wZxA2P3HCMtV+OVLIrAOMBYF1L4RwEe7BQpy3s7McJ5K3cbPgfk4A=="
}

'''


@APP.route("/user/resetpassword", methods=['POST'])
def http_user_reset_password():
    data = request.get_json()

    user_reset_password(
        int(data['user_id']), data['old_password'], data['new_password'], data['token'])

    return {}


'''
json format
{
  "email":"",
  "validation":"",
  "new_password": ""
}
'''
@APP.route("/user/forgetpassword", methods=['POST'])
def http_user_forget_password():
    data = request.get_json()

    user_forget_password(
        data['email'], data['validation'], data['new_password'])

    return {}


'''
json format
{
  "user_id":
  "token"
}
'''


@APP.route("/user/detail", methods=['GET'])
def http_user_detail():
    data = request.args

    result = user_detail(int(data.get('user_id')), data.get('token'))
    return dumps(result)


@APP.route("/user/detail/public", methods=['GET'])
def http_user_detail_public():
    data = request.args
    result = user_detail_public(int(data.get('user_id')))
    return dumps(result)


'''
json format
{
  "user_id":1,
  "first_name":"lisa",
  "last_name":"li",
  "address":"sydney"
  "token"
}
'''


@APP.route("/user/detailupdate", methods=['POST'])
def http_user_detail_update():
    data = request.get_json()

    user_detail_update(int(data['user_id']), data['first_name'],
                       data['last_name'], data['address'], data['token'])

    return {}


'''
json format
{
  "user_id":
  "token"
}
'''


@APP.route("/user/allnotifications", methods=['POST'])
def http_user_all_notifications():
    data = request.get_json()
    u_id = data.get('user_id')
    token = data.get('token')
    result = user_all_notifications(int(u_id), token)
    return dumps(result)


@APP.route("/user/unreadnotifications", methods=['POST'])
def http_user_read_notifications():
    data = request.get_json()
    result = user_read_notification(
        int(data['user_id']), data['notification_id'], data['token'])
    return dumps(result)


@APP.route("/user/deletenotification", methods=['POST'])
def http_user_delete_notification():
    data = request.get_json()
    user_DELETE_notification(int(data['user_id']), int(
        data['notification_id']), data['token'])
    return {}


'''
json format
{
  "activity_id":1,
  "user_id":1,
  "seat_x":10,
  "seat_y":10,
  "token"
}

'''


@APP.route("/user/activitybook", methods=['POST'])
def http_user_activity_book():
    data = request.get_json()

    result = user_book_activity(int(data['activity_id']), int(
        data['user_id']), data['seat_x'], data['seat_y'], data['token'])

    return dumps(result)


'''
json format
{
  "user_id":1,
  "activity_id":1,
  "token"
}

'''


@APP.route("/user/cancel", methods=['POST'])
def http_user_cancel_activity():
    data = request.get_json()

    user_cancel_activity(int(data['user_id']), int(
        data['activity_id']), int(data['booking_id']), data['token'])

    return {}


'''
json format
{
  "user_id":1,
  "money":666666,
  "token"
}
'''


@APP.route("/user/addbalance", methods=['POST'])
def http_user_add_balance():
    data = request.get_json()

    user_add_balance(int(data['user_id']), int(data['money']), data['token'])

    return {}


'''
json format
{
  "user_id":
  "token"
}
'''


@APP.route("/user/listactivities", methods=['GET'])
def http_user_list_activities():
    data = request.args
    doing_check(12)
    result = user_list_activities(int(data.get('user_id')), data.get('token'))
    return dumps(result)


'''
json format
{
  "user_id":1,
  "host_id":1,
   "token" : "6iyUeZvpEmnbgfxp7+8/q5u6Yp1uP6EcDnWpGVEaDE6HUcvSrPsfGZpDA+kOVN69Mi77WxempDG/ahhg2vFr/g=="
}
'''


@APP.route("/user/bookhost", methods=['POST'])
def http_user_book_host():
    data = request.get_json()
    user_book_host(int(data['user_id']), int(data['host_id']), data['token'])

    return {}


@APP.route("/user/isbookhost", methods=['GET'])
def http_user_is_book_host():
    data = request.args
    result = user_check_book_host(int(data.get('user_id')), int(
        data.get('host_id')), data.get('token').replace(" ", "+"))
    return dumps(result)


@APP.route("/user/editaccount", methods=['POST'])
def http_user_edit_account():
    data = request.get_json()
    user_edit_account(
        int(data['user_id']), data['bill_method'], data['account'], data['token'])
    return {}


###############################################
#                 Activity                    #
###############################################

# List all the activities
@APP.route("/activities/listall", methods=['GET'])
def activities_listall():
    detail = request.args
    #token = detail.get('token')
    #u_id = int(detail.get('user_id'))
    sort_by = detail.get('sort_by')
    kind = detail.get('kind')

    activities_list = listAll_activity(sort_by, kind)
    return dumps(activities_list)

# List all the activities


@APP.route("/activities/listallavaiable", methods=['GET'])
def activities_listall_avaiable():
    activities_list = listAll_avaiable_activity()
    return dumps(activities_list)

# List one activity that user has joined


@APP.route("/user/activities/list", methods=['GET'])
def activities_detail():

    detail = request.args
    a_id = detail['a_id']
    activity_list = one_activity_detail(a_id)
    return dumps(activity_list)


# Search activity by given name or part name
@APP.route("/activities/search", methods=['GET'])
def activities_search():
    detail = request.args
    name = detail.get('name')
    description = detail.get('description')
    type = detail.get('type')
    activity_search_list = searchAct(name, description, type)
    return dumps(activity_search_list)

# List all the commits of one activity


@APP.route("/activities/commit/listall", methods=['POST'])
def activities_commit_listAll():
    detail = request.get_json()
    a_id = detail.get('a_id')
    commit_listAll = list_all_commit(a_id)
    return dumps(commit_listAll)


# Add user commit
@APP.route("/activities/commit/add", methods=['POST'])
def activities_commit_userAdd():
    detail = request.get_json()

    if detail['host_id'] == '':
        commit_Add = addCommit(detail['token'], None, int(
            detail['user_id']), detail['message'], detail['a_id'], detail['rating'])
    else:
        commit_Add = addCommit(detail['token'], int(
            detail['host_id']), None, detail['message'], detail['a_id'], None)
    return dumps(commit_Add)


# Edit user commit
@APP.route("/activities/commit/edit", methods=['POST'])
def activities_commit_userEdit():
    detail = request.get_json()

    if detail['host_id'] == '':
        commit_userEdit = editCommit(detail['token'], None, int(
            detail['user_id']), detail['message'], detail['a_id'], detail['c_id'])
    else:
        commit_userEdit = editCommit(detail['token'], int(
            detail['host_id']), None, detail['message'], detail['a_id'], detail['c_id'])
    return dumps(commit_userEdit)

# Remove user commit


@APP.route("/activities/commit/remove", methods=['POST'])
def activities_commit_userRemove():
    detail = request.get_json()

    if detail['host_id'] == '':
        commit_Remove = removeCommit(detail['token'], None, int(
            detail['user_id']), detail['a_id'], detail['c_id'])
    else:
        commit_Remove = removeCommit(detail['token'], int(
            detail['host_id']), None, detail['a_id'], detail['c_id'])
    return dumps(commit_Remove)

# User reply commit


@APP.route("/activities/commit/reply", methods=['POST'])
def activities_commit_userReply():
    detail = request.get_json()

    if detail['host_id'] == '':
        commit_Reply = ReplyCommit(detail['token'], None, int(
            detail['user_id']), detail['message'], detail['a_id'], detail['c_id'])
    else:
        commit_Reply = ReplyCommit(detail['token'], int(
            detail['host_id']), None, detail['message'], detail['a_id'], detail['c_id'])
    return dumps(commit_Reply)

# Reply message


@APP.route("/activities/commit/replyReceive", methods=['POST'])
def activities_commit_replyReceive():
    detail = request.get_json()

    if detail['host_id'] == '':
        commit_replyReceive = replyReceive(
            detail['token'], None, int(detail['user_id']), detail['c_id'])
    else:
        commit_replyReceive = replyReceive(detail.get(
            'token'), detail.get('host_id'), None, detail.get('c_id'))
    return dumps(commit_replyReceive)


@APP.route("/clear/v1", methods=["DELETE"])
def http_clear_v1():
    return dumps(clear_v1())


@APP.route("/clear/token", methods=["GET"])
def http_clear_token():

    return dumps(clear_token())


###############################################
#              Recommendation                 #
###############################################

# User get recommended by the website
@APP.route("/activities/user/recommended", methods=['GET'])
def http_user_get_recommended():
    detail = request.args

    token = detail.get('token')
    u_id = int(detail.get('user_id'))
    if token == None or u_id == None:
        doing_check(12)
        return dumps({})
    doing_check(12)
    activities_info = user_get_recommended(u_id, token)

    return dumps(activities_info)


@APP.route("/activities/user/getpopular", methods=['GET'])
def http_user_get_popular():

    activities_info = acts_get_popular()

    return dumps(activities_info)


@APP.route("/activities/user/descriptionrecommend", methods=['GET'])
def http_user_get_description_recommend():
    detail = request.args

    token = detail.get('token')
    u_id = int(detail.get('user_id'))
    if token == None or u_id == None:
        return dumps({})
    doing_check(2)
    activities_info = get_description_recommended(u_id, token)

    return dumps(activities_info)


# time
"""
    {
      "time": "2017-10-10 10:00:00"
    }
"""


@APP.route("/time/set/now", methods=['POST'])
def http_time_set_now():
    detail = request.get_json()
    time1 = detail.get('time')
    time_set_now(time1)
    return dumps({})


@APP.route("/time/get/now", methods=['GET'])
def http_time_get_now():
    time2 = time_get_now()
    time2['time'] = str(time2['time'])
    return dumps(time2)


"""{
      "week": 52,
      "day": 1,
      "time": 1,
  }
"""


@APP.route("/time/push/now", methods=['POST'])
def http_time_push_now():
    detail = request.get_json()
    time_now = time_push_now(detail)
    time_now['time'] = str(time_now['time'])
    return dumps(time_now)


@APP.route("/time/check", methods=['POST'])
def http_time_check():
    detail = request.get_json()
    detail = detail.get('time')
    time_after_now(detail)
    return dumps({})


@APP.route("/user/name", methods=['POST'])
def http_user_name():
    detail = request.get_json()
    u_id = int(detail.get('user_id'))
    name = get_user_name_server(u_id)
    return dumps(name)


@APP.route("/host/name", methods=['POST'])
def http_host_name():
    detail = request.get_json()
    id = detail.get('host_id')
    h_id = int(id)
    name = get_host_email_server(h_id)
    return dumps(name)


@APP.route("/act/seat", methods=['GET'])
def http_list_act_seat():
    detail = request.args
    id = detail.get('act_id')
    data = list_seat(id)
    return dumps(data)


@APP.route("/overall/info", methods=['GET'])
def http_overall_info():
    data = overall_information()
    return dumps(data)


@APP.route("/host/fan", methods=['GET'])
def http_host_fan():
    data = request.args
    result = host_fan(int(data.get('host_id')),
                      data.get('token').replace(" ", "+"))

    return dumps(result)


if __name__ == "__main__":
    APP.run(port=port, threaded=False)  # Do not edit this port
    print("Server started on port 5000")
