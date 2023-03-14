import datetime

from data_sql import dm
from helper import *
from timeset import *
from error import *


data_manager = dm


# To sign up as a user, need to provide a valid email as username, a password, first name, last
# name, address, bill method, and an account. When the signup information is sent to backend,
# backend would first check whether the email format is valid and check through database
# whether the email has already been used to sign up. If both do not fail, a user should be signed
# up successfully and directed to login page.
def user_signup(user_info):

    check_email(user_info['email'])
    h_id = data_manager.get_hid_by_email(user_info['email'])

    u_id = data_manager.get_uid_by_email(user_info['email'])
    password = user_info["password"]
    user_info["password"] = encode_password(user_info["password"])
    if u_id is None and h_id is None:
        u_id = data_manager.add_user(user_info)
    else:
        raise AccessError('customer already exists')

    time = time_get_now()['time']
    notification = {
        'u_id': u_id,
        'message': 'Welcome, u are a new user!',
        'time': time
    }
    data_manager.add_commit_notifications(notification)

    # return encode_id_backend(u_id)
    token = data_manager.login_user(u_id)
    return {
        "user_id": encode_id_backend(u_id),
        "token": token
    }


# After a user been signed up, can login by using username and password. When the login
# information is sent to backend, backend would check through database whether the username is
# a registered user, and then whether the password is matched. If both passes, then a user will be
# login successfully and be directed to the user page.
def user_login(email, password):

    check_email(email)

    u_id = data_manager.get_uid_by_email(email)

    if not data_manager.is_valid_uid(u_id):
        raise InputError('user does not exist')

    if data_manager.is_active_uid(u_id):
        raise AccessError('already login')

    user = data_manager.get_user_by_uid(u_id)
    if not (user[1] == email and user[2] == encode_password(password)):
        raise InputError('not matched')
    token = data_manager.login_user(u_id)
    return {
        "user_id": encode_id_backend(u_id),
        "token": token
    }


# By clicking the user logout button, backend would check through the database whether the user
# is online. If the user is online, then they should be logout successfully and be redirected to the
# login page.
def user_logout(u_id, token):

    check_uid_token(u_id, token)
    u_id = decode_id_backend(u_id)

    data_manager.logout_user(u_id)
    return True


# By clicking reset password, the user should provide their old password and new password. The
# backend would check through database to check whether the host is online and whether the old
# password matched. If both passes, then the user’s password should be reset successfully.
def user_reset_password(u_id, old_password, new_password, token):

    check_uid_token(u_id, token)
    u_id = decode_id_backend(u_id)

    user = dm.get_user_by_uid(u_id)

    if encode_password(old_password) != user[2]:
        raise InputError('wrong password')

    data_manager.edit_user_password(u_id, encode_password(new_password))
    return {}


# given email, sent validation and new password, by contracting with database,
# user's password can be changed to the new one if validation is correct
def user_forget_password(email, validation, new_password):

    check_email(email)

    u_id = data_manager.get_uid_by_email(email)
    if u_id is None:
        raise InputError('user does not exist')

    if not data_manager.is_valid_uid(u_id):
        raise AccessError('invalid u_id')

    user = data_manager.get_user_by_uid(u_id)
    if user is None:
        raise AccessError('user does not exist')

    got_validation = dm.get_email_validation_by_email(email)
    dm.delete_email_validation_by_uid(email)

    if (got_validation is None) or (got_validation[2] != validation):
        raise AccessError('not matched validation')

    dm.delete_email_validation_by_uid(email)
    data_manager.edit_user_password(u_id, encode_password(new_password))


# By clicking user detail, the user should be online and all the information of the user including
# email, first name, last name, address, bill method, account and balance would be displayed
def user_detail(u_id, token):

    check_uid_token(u_id, token)
    u_id = decode_id_backend(u_id)

    user = data_manager.get_user_by_uid(u_id)
    detail = {
        'u_id': user[0],
        'email': user[1],
        'first_name': user[3],
        'last_name': user[4],
        'address': user[5],
        'bill_method': user[6],
        'account': user[7],
        'token': user[8],
        'balance': user[9]
    }
    return detail


# given uid, return the detail for this user, therefore everyone can see this detail
def user_detail_public(u_id):

    u_id = decode_id_backend(u_id)

    if not data_manager.is_valid_uid(u_id):
        raise AccessError('invalid u_id')

    user = data_manager.get_user_by_uid(u_id)
    detail = {
        'u_id': user[0],
        'email': user[1],
        'first_name': user[3],
        'last_name': user[4],
        'address': user[5],
    }
    return detail


# By clicking user detail update, the user should be online and provide a new first name, last
# name, and address to update the detail.
def user_detail_update(u_id, first_name, last_name, address, token):

    check_uid_token(u_id, token)
    u_id = decode_id_backend(u_id)

    user = data_manager.get_user_by_uid(u_id)

    updated_user = {}
    updated_user['email'] = user[1]

    if first_name != None:
        updated_user['name_first'] = first_name
    if last_name != None:
        updated_user['name_last'] = last_name
    if address != None:
        updated_user['address'] = address

    data_manager.edit_user(u_id, updated_user)

    return {}


# By clicking all notifications, the user should be online, and all notifications of the user would
# be displayed with unread notifications be marked.
def user_all_notifications(u_id, token):

    check_uid_token(u_id, token)
    u_id = decode_id_backend(u_id)

    notifications = data_manager.get_all_notifications_by_uid(u_id)
    if notifications is None:
        notifications = ()
    unread_notifications = data_manager.get_unread_notifications_by_uid(u_id)
    if unread_notifications is None:
        unread_notifications = 0
    else:
        unread_notifications = len(unread_notifications)
    message = []

    for notification in notifications:
        # message.append(notification[2])
        dictA = {
            "id": notification[0],
            "act_id": notification[3],
            "message": notification[2],
            "is_read": notification[4],
            "time": str(notification[5]),
        }
        message.append(dictA)

    return {
        'notifications': message,
        'unread_notifications': unread_notifications
    }


# user click the notification, the notification would be marked as read
def user_read_notification(u_id, notification_id, token):

    check_uid_token(u_id, token)
    u_id = decode_id_backend(u_id)

    if (type(notification_id) != int):
        notification_id = int(notification_id)

    data_manager.update_notifications_by_nid(notification_id)
    return {}


# user can edit their payment method through given uid , bill method,account and token
# the user must be online
def user_edit_account(u_id, bill_method, account, token):

    check_uid_token(u_id, token)
    u_id = decode_id_backend(u_id)
    data_manager.edit_user_payment(u_id, bill_method, account)
    return {}


# By clicking book activity, the user should choose an activity and choose a seat. If the money in
# their account is enough, then the activity will be booked successfully. If not, then they need to
# add balance and then book the activity again. If the seat is full, then they need to choose another
# seat to book
def user_book_activity(act_id, u_id, seat_x, seat_y, token):

    check_uid_token(u_id, token)
    u_id = decode_id_backend(u_id)

    if not data_manager.is_valid_aid(act_id):
        raise AccessError('Not a act')

    activity = data_manager.get_act_by_aid(act_id)
    if activity is None:
        raise AccessError('wrong activity id')

    # check time
    now = time_get_now()['time']
    activity_time = (datetime.datetime.min + activity[7]).time()
    activity_date = activity[9]

    if now > datetime.datetime.combine(activity_date, activity_time):
        raise AccessError('cannot book and act begin')

    ticket_money = activity[13]
    activity_seat_x = activity[14]
    activity_seat_y = activity[15]

    try:
        seat_x = int(seat_x)
    except:
        raise AccessError('seat_x is not int')

    try:
        seat_y = int(seat_y)
    except:
        raise AccessError('seat_y is not int')

    if seat_x > activity_seat_x:
        raise AccessError('seat_x exceeds')
    if seat_y > activity_seat_y:
        raise AccessError('seat_y exceeds')

    if seat_x < 1:
        raise AccessError('seat_x less than 1')
    if seat_y < 1:
        raise AccessError('seat_1 less than 1')

    if activity[11] <= 0:
        raise AccessError('full seat')
    seat_not_full = data_manager.is_seat_not_full_by_act_id(
        act_id, seat_x, seat_y)
    if not seat_not_full:
        raise AccessError('This seat is booked')

    if not data_manager.is_enough_balance_by_uid(u_id, ticket_money):
        raise AccessError('no money')

    booking_id = data_manager.add_user_to_act(act_id, u_id, seat_x, seat_y)
    ticket_money = - ticket_money
    data_manager.edit_balance_by_uid(u_id, ticket_money)

    time = time_get_now()['time']
    notification = {
        'u_id': u_id,
        'act_id': act_id,
        'message': 'You buy a new activity: ' + activity[2] + '!    \n\t ' + "We happy to see you here!",
        'time': time
    }
    data_manager.add_notifications(notification)

    return booking_id


# By clicking cancel activity, the user should be online, and the date should be 7 days before the
# activity begins. If both satisfy, then the user cancels this activity and gets money back to their
# account.
def user_cancel_activity(u_id, act_id, booking_id, token):

    check_uid_token(u_id, token)
    u_id = decode_id_backend(u_id)

    if not data_manager.is_valid_aid(act_id):
        raise AccessError('invalid act_id')

    # check time

    activity = data_manager.get_act_by_aid(act_id)

    now = time_get_now()['time']
    activity_time = (datetime.datetime.min + activity[7]).time()
    activity_date = activity[9]

    if now + datetime.timedelta(days=7) > datetime.datetime.combine(activity_date, activity_time):
        raise AccessError('cannot cancel within 7 days')

    ticket_money = activity[13]
    data_manager.remove_use_from_act(act_id, booking_id, u_id)
    data_manager.edit_balance_by_uid(u_id, ticket_money)
    time = time_get_now()['time']
    notification = {
        'u_id': u_id,
        'act_id': act_id,
        'message': 'You cancel a new activity: ' + data_manager.get_act_by_aid(act_id)[2] + '!   \n\t' + 'You will get your money back soon.',
        'time': time
    }
    data_manager.add_notifications(notification)


# By clicking add balance, the user should be online, and money should be greater than 0. If both
# satisfy, then money will be added to the user’s account.
def user_add_balance(u_id, money, token):

    check_uid_token(u_id, token)
    u_id = decode_id_backend(u_id)

    if money < 0:
        raise AccessError('invalid money')

    data_manager.edit_balance_by_uid(u_id, money)
    time = time_get_now()['time']
    notification = {
        'u_id': u_id,
        'message': 'You have added $' + str(money) + ' to your account',
        'time': time
    }
    data_manager.add_commit_notifications(notification)


# the user must be online and through this method, they can book a host
# by given their hid, then the user would be one of the fan of this host
def user_book_host(u_id, h_id, token):

    check_uid_token(u_id, token)

    u_id = decode_id_backend(u_id)
    h_id = decode_id_backend(h_id)

    if not data_manager.is_valid_hid(h_id):
        raise AccessError('invalid h_id')
    if data_manager.is_sub_uid_hid(u_id, h_id):
        data_manager.delete_host_sub(u_id, h_id)
    else:
        dm.add_host_sub(u_id, h_id)
    return {}


# the user must be online and by knowing the host's id, they can check
# whether they have successsfully book the host
def user_check_book_host(u_id, h_id, token):

    check_uid_token(u_id, token)
    u_id = decode_id_backend(u_id)
    h_id = decode_id_backend(h_id)
    return {"boolean": data_manager.is_sub_uid_hid(u_id, h_id)}


# the user must be online and by knowing the notification id, they can delete
# this notification from the notification list
def user_DELETE_notification(u_id, noti_id, token):

    check_uid_token(u_id, token)

    u_id = decode_id_backend(u_id)

    if not data_manager.is_user_notification(u_id, noti_id):
        raise AccessError('not notification')
    data_manager.delete_notification(noti_id)
    return {}
