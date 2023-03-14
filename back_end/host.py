import smtplib
import random
import datetime

from data_sql import dm
from email.mime.text import MIMEText
from email.header import Header
from helper import *
from error import *
from timeset import time_get_now

data_manager = dm


# To sign up as a host, need to provide a valid email as a username and a password. When the
# signup information is sent to the backend, the backend would first check whether the email
# format is valid and check through the database whether the email has already been used to sign
# up. If both do not fail, a host should be signed up successfully and directed to the login page.
def host_signup(email, password):

    check_email(email)

    h_id = data_manager.get_hid_by_email(email)
    if h_id is not None:
        raise AccessError('host already exists')
    u_id = data_manager.get_uid_by_email(email)
    if u_id is not None:
        raise AccessError('user already exists')

    host = {}
    host['email'] = email
    host['password'] = encode_password(password)
    h_id = data_manager.add_host(host)

    # return encode_id_backend(h_id)

    token = data_manager.login_host(h_id)
    return {
        "host_id": encode_id_backend(h_id),
        "token": token
    }


# After a host has been signed up, can log in by using a username and password. When the login
# information is sent to the backend, the backend would check through the database whether the
# username is a registered host, and then whether the password is matched. If both passes, then a
# host will be login successfully and be directed to the host page.
def host_login(email, password):

    check_email(email)

    h_id = data_manager.get_hid_by_email(email)
    if h_id is None:
        raise InputError('host does not exist')

    if not data_manager.is_valid_hid(h_id):
        raise AccessError('invalid h_id')

    if data_manager.is_active_hid(h_id):
        raise AccessError('already login')

    host = data_manager.get_host_by_hid(h_id)
    if not (host[1] == email and host[2] == encode_password(password)):
        raise InputError('not matched')
    token = data_manager.login_host(h_id)
    return {
        "host_id": encode_id_backend(h_id),
        "token": token
    }


# By clicking the host logout button, the backend would check through the database whether the
# host is online. If the host is online, then they should be logout successfully and redirected to the
# login page.
def host_logout(h_id, token):
    #h_id = data_manager.get_hid_by_email(email)

    check_hid_token(h_id, token)
    h_id = decode_id_backend(h_id)

    data_manager.logout_host(h_id)

    return True


# By clicking reset password, the host should provide their old password and new password. The
# backend would check through the database to check whether the host is online and whether the
# old password matched. If both passes, then the host’s password should be reset successfully
def host_reset_password(h_id, old_password, new_password, token):

    check_hid_token(h_id, token)
    h_id = decode_id_backend(h_id)

    host = dm.get_host_by_hid(h_id)

    if encode_password(old_password) != host[2]:
        raise InputError('wrong password')

    data_manager.edit_host_password(h_id, encode_password(new_password))
    return {}


# By clicking forget password, the host should provide their email and a validation code. The
# backend would check through the database to check whether the host is online and whether the
# email is valid. If both passes, then the host should be able to reset their password.
def host_forget_password(email, validation, new_password):

    check_email(email)

    h_id = data_manager.get_hid_by_email(email)
    if h_id is None:
        raise InputError('host does not exist')

    if not data_manager.is_valid_hid(h_id):
        raise AccessError('invalid h_id')

    host = data_manager.get_host_by_hid(h_id)
    if host is None:
        raise AccessError('host does not exist')

    got_validation = dm.get_email_validation_by_email(email)
    dm.delete_email_validation_by_uid(email)

    if (got_validation is None) or (got_validation[2] != validation):
        raise AccessError('not matched validation')

    data_manager.edit_host_password(h_id, encode_password(new_password))


# When creating a new activity, a host should provide:
# activity name, activity description, activity type, venue name, venue address, start time, end
# time, start date, end date, ticket number, possible seats, ticket money, the row number of seats,
# and column number of seats. The backend would check whether the host is online and whether the start date and start time
# are after time now. If both satisfy, then create the new activity according to the activity
# information.
def host_new_activity(h_id, activity, token):

    check_hid_token(h_id, token)
    h_id = decode_id_backend(h_id)

    if 'type' not in activity or activity['type'] == "":
        raise InputError('invalid type')

    if 'image' not in activity:
        activity['image'] = None

    now = time_get_now()['time']
    start = datetime.datetime.combine(
        activity['start_date'], activity['start_time'])
    if now > start:
        raise InputError('Invalid start time!')

    end = datetime.datetime.combine(activity['end_date'], activity['end_time'])
    if start > end:
        raise InputError('Invalid end time!')

    activity['host_id'] = h_id
    act_id = data_manager.add_act(activity)

    subed_users = data_manager.get_user_sub_by_hid(h_id)
    if subed_users is not None:

        for subed_user in subed_users:
            time = time_get_now()['time']
            notification = {
                'u_id': subed_user[2],
                'act_id': act_id,
                'message': 'A new activity related to ' + data_manager.get_host_by_hid(h_id)[1] + ' has been released',
                'time': time
            }
            data_manager.add_notifications(notification)

    return act_id


# When canceling an activity, the backend would check whether the host is online and whether
# the activity has already begun. If both passes, then the activity should be cancelled, and all
# customers within the activity would be formed a notification their money would be refunded to
# their account.
def host_cancel_activity(h_id, act_id, token):

    check_hid_token(h_id, token)
    h_id = decode_id_backend(h_id)

    if not data_manager.is_valid_aid(act_id):
        raise AccessError('invalid act_id')

    # check time
    activity = data_manager.get_act_by_aid(act_id)

    now = time_get_now()['time']
    activity_time = (datetime.datetime.min + activity[7]).time()
    activity_date = activity[9]

    if now > datetime.datetime.combine(activity_date, activity_time):
        raise AccessError('cannot cancel within 7 days')

    ticket_money = activity[13]

    users = data_manager.list_all_users_by_act(act_id)
    if users is None:
        users = ()

    message = "Sorry your" + activity[2] + "is canceled"
    time_add = time_get_now()['time']
    for user in users:
        u_id = user[3]
        data_manager.remove_this_user_from_act(act_id, u_id)
        data_manager.edit_balance_by_uid(u_id, ticket_money)
        notification = {
            'u_id': u_id,
            'act_id': act_id,
            'message': message,
            'time': time_add
        }
        data_manager.add_notifications(notification)
    data_manager.remove_act(act_id)

    return True


# Clicking broadcast notification, choosing an activity, and entering a message, if the host is
# online, then the message would be broadcast as a notification to all customers within the
# activity
def host_broadcast_notification(h_id, act_id, message, token):

    check_hid_token(h_id, token)
    h_id = decode_id_backend(h_id)

    time = time_get_now()['time']

    users = data_manager.list_all_users_by_act(act_id)
    if users == None:
        users = ()
    act_name = data_manager.get_act_by_aid(act_id)[2]
    message2 = "Host: " + data_manager.get_host_by_hid(
        h_id)[1] + " broadcast: " + message + " in Act:" + act_name + "!"
    for user in users:
        u_id = user[3]
        notification = {
            'u_id': u_id,
            'act_id': act_id,
            'message': message2,
            'time': time
        }
        data_manager.add_notifications(notification)

    notification2 = {
        "act_id": act_id,
        "message": message,
        "time": time
    }

    data_manager.add_notifications_host(notification2)
    return {}


# given a host's hid, an online user can get
# detail of this host: activities, email and whether has
# been book
def host_detail(h_id, u_id, token):
    """
    {
    "can_book" : bool
    "is booked" : bool
    "email" : str
    "list of act": [act]    

    }

    """
    check_uid_token(u_id, token)

    u_id = decode_id_backend(u_id)

    is_booked = False
    h_id = decode_id_backend(h_id)
    if not data_manager.is_valid_hid(h_id):
        raise AccessError('invalid h_id')

    email_data = data_manager.get_host_by_hid(h_id)[1]
    activities_info = []
    data1 = data_manager.get_act_info_by_hid(h_id)
    if data1 is None:
        data1 = ()
    count = 1
    for act in data1:
        activity = tuple_act_to_list(act, (), ())
        if activity['name'] != 'DELETE ALREADY':
            activity['act_id'] = activity['id']
            activity['id'] = count
            activity['ticket_money'] = '$' + str(activity['ticket_money'])
            activities_info.append(activity)
            count += 1

    is_booked = data_manager.is_sub_uid_hid(u_id, h_id)

    return {
        "is_booked": is_booked,
        "email": str(email_data),
        "list_of_act": activities_info
    }


# the host must be online, and this method would return
# all fans of this host
def host_fan(h_id, token):

    check_hid_token(h_id, token)
    h_id = decode_id_backend(h_id)

    data1 = data_manager.get_user_sub_by_hid(h_id)
    list_a = []
    if data1 is None:
        data1 = ()
    for i in data1:
        uid = i[2]
        user_info = data_manager.get_user_by_uid(uid)
        dict_user = {
            'email': user_info[1],
            'first_name': user_info[3],
            'last_name': user_info[4]
        }
        list_a.append(dict_user)
    return list_a


#############################################
# HELPER
################################################

# this method random generate a six character validation
# and then add this validation to database matching a given email
def add_validation(email):

    all_letters = []
    for upper_case in range(65, 91):
        all_letters.append(chr(upper_case))
    for lower_case in range(97, 123):
        all_letters.append(chr(lower_case))
    for number in range(48, 58):
        all_letters.append(chr(number))
    six_letters = random.sample(all_letters, 6)
    validation = "".join(six_letters)

    dm.add_email_validation(email, validation)

    return validation


# given a email, add a matched validation to database and
# send this validation to this email
def send_email(email):

    dm.delete_email_validation_by_uid(email)
    validation = add_validation(email)

    email_host = "smtp.163.com"
    email_sender = "Comp3900sender1@163.com"
    sender_code = "CPNEZWHRFGZGEVVO"

    receiver = [email]

    message = MIMEText(validation, 'plain', 'utf-8')
    message['From'] = Header("3900", 'utf-8')
    message['To'] = Header("3900", 'utf-8')

    subject = 'validation for reset new password'
    message['Subject'] = Header(subject, 'utf-8')

    smtpObject = smtplib.SMTP()
    smtpObject.connect(email_host, 25)
    smtpObject.login(email_sender, sender_code)
    smtpObject.sendmail(email_sender, receiver, message.as_string())
