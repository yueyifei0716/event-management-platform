import pytest
from ListActs import *
from user import *
from host import *
from data_sql import dm
from other import *
from test_accounts import *
import datetime




def test_user_signup():
    
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)
    
    user = user_signup_info666()
    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id = encode_id_frontend(u_id)
    token = login_return["token"]
    assert(type(u_id) == int)

    #sign up again
    with pytest.raises( AccessError):
        user_signup(user)


def test_user_login():

    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    #login before signup
    with pytest.raises( InputError):
        user_login('1111a@163.com', '111a@163.com')
    
    user = user_signup_info666()
    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id = encode_id_frontend(u_id)
    token = login_return["token"]
    user_logout(u_id, token)

    #wrong password
    with pytest.raises( InputError):
        user_login('1111a@163.com', '112a')

    login_return = user_login('1111a@163.com', '111a@163.com')
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id = encode_id_frontend(u_id)
    token = login_return["token"]
    assert(type(u_id) == int)

    with pytest.raises( AccessError):
        user_login('1111a@163.com', '111a@163.com')

def test_host_logout():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    #not login
    # with pytest.raises( AccessError):
    #     user_logout(200000001, 1)

    user = user_signup_info666()


    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id = encode_id_frontend(u_id)
    token = login_return["token"]

    #not exist
    # with pytest.raises( AccessError):
    #     user_logout(200000001, 1)

    boolean = user_logout(u_id, token)

    assert(boolean == True)

def test_user_reset():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    user = user_signup_info666()

    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id = encode_id_frontend(u_id)
    token = login_return["token"]


    #wrong old password
    with pytest.raises( InputError):
        user_reset_password(u_id, 'aaa', '111a@163.com', token)

    user_reset_password(u_id, '111a@163.com', 'aaa', token)

    user_logout(u_id, token)
    login_return = user_login('1111a@163.com', 'aaa')
    
    u_id = login_return["user_id"]
    assert(type(u_id) == int)

def test_user_forget():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    user = user_signup_info666()

    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id = encode_id_frontend(u_id)
    token = login_return["token"]
    user_logout(u_id, token)

    validation = add_validation('1111a@163.com')

    with pytest.raises( InputError):
        user_forget_password('1111aa@163.com', '111', 'aaa')

    user_forget_password('1111a@163.com', validation, 'aaa')

    with pytest.raises( AccessError):
        user_forget_password('1111a@163.com', '111', 'aaa')

    login_return = user_login('1111a@163.com', 'aaa')
    
    u_id = login_return["user_id"]
    assert(type(u_id) == int)


def test_user_user_add_balance():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    user = user_signup_info666()

    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id = encode_id_frontend(u_id)
    token = login_return["token"]

    with pytest.raises( AccessError):
        user_add_balance(u_id, -1000, token)

    user_add_balance(u_id, 1000, token)

def test_user_book1():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)


    login_return = host_signup('111a@163.com', '111a@163.com')
    h_id = login_return["host_id"]
    h_id = decode_id_frontend(h_id)
    h_id = encode_id_frontend(h_id)
    token = login_return["token"]
    
    act = activity_create_info(h_id)
    act_id = host_new_activity(h_id, act, token)

    user = user_signup_info666()
    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id = encode_id_frontend(u_id)
    token = login_return["token"]

    with pytest.raises( AccessError):
        user_book_activity(act_id, u_id, 10, 10, token)

    user_add_balance(u_id, 1000, token)

    with pytest.raises( AccessError):
        user_book_activity(6, u_id, 10, 10, token)

    date = "2018-09-1 18:05:44"    
    time_set_now(date)   
    with pytest.raises( AccessError):
        user_book_activity(act_id, u_id, 10, 10, token)
    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    with pytest.raises( AccessError):
        user_book_activity(act_id, u_id, 100, 10, token)

    with pytest.raises( AccessError):
        user_book_activity(act_id, u_id, 10, 100, token)

    b_id = user_book_activity(act_id, u_id, 10, 10, token)
    assert(type(b_id) == int)

def test_user_activities():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    login_return = host_signup('111a@163.com', '111a@163.com')
    h_id = login_return["host_id"]
    h_id = decode_id_frontend(h_id)
    h_id = encode_id_frontend(h_id)
    h_token = login_return["token"]
    
    act = activity_create_info(h_id)
    act_id = host_new_activity(h_id, act, h_token)


    user = user_signup_info666()
    
    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id = encode_id_frontend(u_id)
    token = login_return["token"]    
    user_add_balance(u_id, 1000, token)

    #before book, all activities information should be empty
    activities_info = user_list_activities(u_id, token)
    assert(activities_info['activities_info'] == [])

    user_book_activity(act_id, u_id, 10, 10, token)
    activities_info = user_list_activities(u_id, token)
    assert(activities_info['activities_info'][0]['name'] == 'andy')
    detail = user_detail(u_id, token)
    assert(detail['balance'] == 800)

    host_list_activities(h_id, h_token)

    with pytest.raises( AccessError):
        user_book_activity(act_id, u_id, 10, 10, token)



def test_user_detail():

    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    user = user_signup_info666()

    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id = encode_id_frontend(u_id)
    token = login_return["token"]  

    detail = user_detail(u_id,token)
    assert(detail['first_name'] == 'andy')
    assert(detail['account'] == '111a@163.com')
    #assert(detail['token'] == 0)



def test_user_all_notifications():

    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    
    login_return = host_signup('111a@163.com', '111a@163.com')
    h_id = login_return["host_id"]
    h_id = decode_id_frontend(h_id)
    h_id = encode_id_frontend(h_id)
    h_token = login_return["token"]

    act = activity_create_info(h_id)
    act_id = host_new_activity(h_id, act, h_token)

    user = user_signup_info666()
    
    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id = encode_id_frontend(u_id)
    token = login_return["token"]  
    

    all_notifications = user_all_notifications(u_id,token)
    assert(len(all_notifications['notifications']) == 1)
    assert(all_notifications['unread_notifications'] == 1)

    user_add_balance(u_id, 1000, token)
    user_book_activity(act_id, u_id, 10, 10, token)

    host_broadcast_notification(h_id, act_id, 'hello', h_token)
    host_broadcast_notification(h_id, act_id, 'world', h_token)

    all_notifications = user_all_notifications(u_id, token)
    assert(all_notifications['notifications'][4]['message'] == 'Host: 111a@163.com broadcast: world in Act:andy!')
    assert(all_notifications['unread_notifications'] == 5)
    user_read_notification(u_id, all_notifications['notifications'][2]['id'], token)
    all_notifications = user_all_notifications(u_id, token)
    assert(all_notifications['notifications'][4]['message'] == 'Host: 111a@163.com broadcast: world in Act:andy!')
    assert(all_notifications['unread_notifications'] == 4) 
    user_DELETE_notification(u_id, all_notifications['notifications'][1]['id'], token)
    all_notifications = user_all_notifications(u_id, token)
    assert(all_notifications['unread_notifications'] == 3) 


def test_user_update_detail():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    user = user_signup_info666()
    
    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id = encode_id_frontend(u_id)
    token = login_return["token"]  

    user_detail_update(u_id, 'ali', 'li', 'beijing', token)
    detail = user_detail(u_id,token)
    assert(detail['first_name'] == 'ali')
    assert(detail['last_name'] == 'li')
    assert(detail['address'] == 'beijing')


def test_user_cancel():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    
    login_return = host_signup('111a@163.com', '111a@163.com')
    h_id = login_return["host_id"]
    h_id = decode_id_frontend(h_id)
    h_id = encode_id_frontend(h_id)
    token = login_return["token"]
    
    act = activity_create_info(h_id)
    act_id = host_new_activity(h_id, act, token)

    user = user_signup_info666()
    
    
    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id = encode_id_frontend(u_id)
    token = login_return["token"]

    user_add_balance(u_id, 1000, token)
    booking_id = user_book_activity(act_id, u_id, 10, 10, token)

    activities_info = user_list_activities(u_id, token)
    assert(len(activities_info['activities_info']) == 1)

    with pytest.raises( AccessError):
        user_cancel_activity(u_id, 6, booking_id, token)

    date = "2018-07-29 18:05:44"    
    time_set_now(date)

    with pytest.raises( AccessError):
        user_cancel_activity(u_id, act_id, booking_id, token)

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    user_cancel_activity(u_id, act_id, booking_id, token)
    detail = user_detail(u_id, token)
    assert(detail['balance'] == 1000)

    activities_info = user_list_activities(u_id, token)
    assert(len(activities_info['activities_info']) == 0)



def test_user_edit():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    user = user_signup_info666()
    
    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id = encode_id_frontend(u_id)
    token = login_return["token"] 

    user_edit_account(u_id, 'wechat', '111', token)
    # user_edit_account(u_id, 'ebay', '11111111', token)
    # user_edit_account(u_id, 'visa', '1111111111111111', token)

def test_user_book():
    
    clear_v1()
    
    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    
    login_return = host_signup('111a@163.com', '111a@163.com')
    h_id = login_return["host_id"]
    h_id = decode_id_frontend(h_id)
    h_id = encode_id_frontend(h_id)
    token = login_return["token"]
    
    user = user_signup_info666()
    
    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id = encode_id_frontend(u_id)
    u_token = login_return["token"]

    user_book_host(u_id, h_id, u_token)
    detail = host_detail(h_id, u_id, u_token)
    assert(detail['is_booked'] == True)
    
    act = activity_create_info(h_id)
    host_new_activity(h_id, act, token)

    all_notifications = user_all_notifications(u_id, u_token)
    assert(all_notifications['unread_notifications'] == 2)

    detail = host_detail(h_id, u_id, u_token)
    assert(detail['is_booked'] == True)

    user_book_host(u_id, h_id, u_token)
    detail = host_detail(h_id, u_id, u_token)
    assert(detail['is_booked'] == False)

def test_user_detail_public():

    clear_v1()
    date = "2018-07-1 18:05:44"    
    time_set_now(date)
    user = user_signup_info666()
    
    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id = encode_id_frontend(u_id)

    detail = user_detail_public(u_id)
    assert(detail['email'] == '1111a@163.com')

def test_user_check_book_host():
    clear_v1()
    
    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    
    login_return = host_signup('111a@163.com', '111a@163.com')
    h_id = login_return["host_id"]
    h_id = decode_id_frontend(h_id)
    h_id = encode_id_frontend(h_id)
    token = login_return["token"]
    
    user = user_signup_info666()
    
    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id = encode_id_frontend(u_id)
    u_token = login_return["token"]

    bool = user_check_book_host(u_id, h_id, u_token)

    assert(bool['boolean'] == False)

    user_book_host(u_id, h_id, u_token)

    bool = user_check_book_host(u_id, h_id, u_token)

    assert(bool['boolean'] == True)