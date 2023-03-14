
import pytest
from ListActs import *
from host import *
from user import *
from other import *
from test_accounts import *
from timeset import *



def test_host_signup():
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

    #sign up again
    with pytest.raises( AccessError):
        host_signup('111a@163.com', '111a@163.com')
    
    #sign up again
    with pytest.raises( AccessError):
        host_signup('1111a@163.com', '111a@163.com')
    


def test_host_login():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    #login before sign up
    with pytest.raises( InputError):
        host_login('111a@163.com', '111a@163.com')

    login_return = host_signup('111a@163.com', '111a@163.com')
    h_id = login_return["host_id"]
    h_id = decode_id_frontend(h_id)
    h_id = encode_id_frontend(h_id)
    token = login_return["token"]
    host_logout(h_id, token)


    #wrong password
    with pytest.raises( InputError):
        host_login('111a@163.com', '112a')

    h_id = host_login('111a@163.com', '111a@163.com')["host_id"]

    with pytest.raises( AccessError):
        host_login('111a@163.com', '111a@163.com')

    assert(type(h_id) == int)


def test_host_logout():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    #not login
    # with pytest.raises( AccessError):
    #     host_logout(200000001 , 1)

    login_return = host_signup('111a@163.com', '111a@163.com')
    h_id = login_return["host_id"]
    h_id = decode_id_frontend(h_id)
    h_id = encode_id_frontend(h_id)
    token = login_return["token"]

    #not exist
    # with pytest.raises( AccessError):
    #     host_logout(200000001, 1)

    boolean = host_logout(h_id, token)
    
    login_return = host_login('111a@163.com', '111a@163.com')
    h_id = login_return["host_id"]
    h_id = decode_id_frontend(h_id)
    h_id = encode_id_frontend(h_id)
    token = login_return["token"]
    boolean = host_logout(h_id, token)

    assert(boolean == True)



    
def test_host_reset():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    login_return = host_signup('111a@163.com', '111a@163.com')
    h_id = login_return["host_id"]
    h_id = decode_id_frontend(h_id)
    h_id = encode_id_frontend(h_id)
    token = login_return["token"]

    #wrong old password
    with pytest.raises( InputError):
        host_reset_password(h_id, 'aaa', '111a@163.com', token)

    host_reset_password(h_id, '111a@163.com', 'aaa', token)

    host_logout(h_id, token)
    login_return = host_login('111a@163.com', 'aaa')
    
    h_id = login_return["host_id"]
    assert(type(h_id) == int)


def test_host_forget():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    login_return = host_signup('111a@163.com', '111a@163.com')
    h_id = login_return["host_id"]
    h_id = decode_id_frontend(h_id)
    h_id = encode_id_frontend(h_id)
    token = login_return["token"]
    host_logout(h_id, token)

    validation = add_validation('111a@163.com')

    with pytest.raises( InputError):
        user_forget_password('1111aa@163.com', '111', 'aaa')

    host_forget_password('111a@163.com', validation, 'aaa')

    with pytest.raises( AccessError):
        host_forget_password('111a@163.com', '111', 'aaa')
        
    login_return = host_login('111a@163.com', 'aaa')
    
    h_id = login_return["host_id"]
    assert(type(h_id) == int)



def test_host_cancel_activity():
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
    activities_info = host_list_activities(h_id, h_token)
    assert(len(activities_info['activities_info']) == 1)

    user = user_signup_info666()
    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id = encode_id_frontend(u_id)
    u_token = login_return["token"]
    user_add_balance(u_id, 1000, u_token)

    user_book_activity(act_id, u_id, 10, 10, u_token)
    user_book_activity(act_id, u_id, 9, 9, u_token)

    date = "2018-08-05 18:05:44"    
    time_set_now(date)
    with pytest.raises( AccessError):
        host_cancel_activity(h_id, act_id, h_token)
    date = "2018-07-1 18:05:44"    
    time_set_now(date)
    
    with pytest.raises( AccessError):
        host_cancel_activity(h_id, 66, h_token)

    host_cancel_activity(h_id, act_id, h_token)
    activities_info = host_list_activities(h_id, h_token)
    assert(len(activities_info['activities_info']) == 0)

    act_id = host_new_activity(h_id, act, h_token)
    activities_info = host_list_activities(h_id, h_token)
    assert(len(activities_info['activities_info']) == 1)


    host_cancel_activity(h_id, act_id, h_token)
    activities_info = host_list_activities(h_id, h_token)
    assert(len(activities_info['activities_info']) == 0)

    activities_info = user_list_activities(u_id, u_token)
    assert(len(activities_info['activities_info']) == 0)



def test_host_list_all_activities():
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

    activities_info = host_list_activities(h_id, token)
    assert(activities_info['activities_info'][0]['name'] == 'andy')
    assert(type(activities_info['activities_info'][0]['start_date']) == str)

def test_host_broadcast():
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
    user_add_balance(u_id, 1000, token)

    user_book_activity(act_id, u_id, 10, 10, token)

    host_broadcast_notification(h_id, act_id, 'hello', h_token)
    host_broadcast_notification(h_id, act_id, 'world', h_token)

    all_notifications = user_all_notifications(u_id, token)
    assert(all_notifications['notifications'][4]['message'] == 'Host: 111a@163.com broadcast: world in Act:andy!')
    assert(all_notifications['unread_notifications'] == 5)


def test_host_new_activity():
    
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

    with pytest.raises( InputError):
        act = activity_create_info8(h_id)
        act_id = host_new_activity(h_id, act, token)
    
    with pytest.raises( InputError):
        act = activity_create_info9(h_id)
        act_id = host_new_activity(h_id, act, token)
    
    act = activity_create_info(h_id)
    act_id = host_new_activity(h_id, act, token)
    assert(type(act_id) == int)

    all_notifications = user_all_notifications(u_id, u_token)
    assert(all_notifications['unread_notifications'] == 2)

def test_host_detail():
    
    clear_v1()
    
    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    login_return = host_signup('111a@163.com', '111a@163.com')
    h_id = login_return["host_id"]
    h_id = decode_id_frontend(h_id)
    h_id = encode_id_frontend(h_id)
    h_token = login_return["token"]
    
    user = user_signup_info666()
    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id = encode_id_frontend(u_id)
    u_token = login_return["token"]

    detail = host_detail(h_id, u_id, u_token)
    assert(detail['is_booked'] == False)


    

    
def test_host_fan_list():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    login_return = host_signup('111a@163.com', '111a@163.com')
    h_id = login_return["host_id"]
    h_id = decode_id_frontend(h_id)
    h_id = encode_id_frontend(h_id)
    h_token = login_return["token"]
    
    user = user_signup_info666()
    
    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id = encode_id_frontend(u_id)
    u_token = login_return["token"]
    
    res = host_fan(h_id, h_token)
    assert(res == [])
    
    user_book_host(u_id, h_id, u_token)
    detail = host_detail(h_id, u_id, u_token)
    assert(detail['is_booked'] == True)
    
    res = host_fan(h_id, h_token)
    assert(len(res) == 1)
    
    user_book_host(u_id, h_id, u_token)
    detail = host_detail(h_id, u_id, u_token)
    res = host_fan(h_id, h_token)
    assert(detail['is_booked'] == False)
    assert(res == [])

