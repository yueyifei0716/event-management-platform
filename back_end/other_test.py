import pytest
from Activity import *
from ListActs import *
from data_sql import dm
from other import *
from host import *
from timeset import time_get_now, time_push_now, time_set_now
from user import *
from test_accounts import *


@pytest.fixture
def basic_info():
    clear_v1()
    date = "2018-07-1 18:05:44"    
    time_set_now(date)    
    
    login = host_signup('422922280@qq.com', '123123')
    login['host_id'] = decode_id_frontend(login['host_id'])
    login['host_id'] = encode_id_frontend(login['host_id'])    
    a_id1 = host_new_activity(login['host_id'], activity_create_info(login['host_id']), login['token'])
    a_id2 = host_new_activity(login['host_id'], activity_create_info(login['host_id']), login['token']) 
    a_id3 = host_new_activity(login['host_id'], activity_create_info(login['host_id']), login['token']) 
    a_id4 = host_new_activity(login['host_id'], activity_create_info(login['host_id']), login['token'])    
    
    user1 = user_signup_info()
    u_id1 = user_signup(user1) 
    u_id1['user_id'] = decode_id_frontend(u_id1['user_id'])
    u_id1['user_id'] = encode_id_frontend(u_id1['user_id'])
    
    user2 = user_signup_info2()
    u_id2 = user_signup(user2) 
    u_id2['user_id'] = decode_id_frontend(u_id2['user_id'])
    u_id2['user_id'] = encode_id_frontend(u_id2['user_id'])    
    
    
    user3 = user_signup_info3()
    u_id3 = user_signup(user3) 
    u_id3['user_id'] = decode_id_frontend(u_id3['user_id'])
    u_id3['user_id'] = encode_id_frontend(u_id3['user_id'])
    
    user4 = user_signup_info4()
    u_id4 = user_signup(user4) 
    u_id4['user_id'] = decode_id_frontend(u_id4['user_id'])
    u_id4['user_id'] = encode_id_frontend(u_id4['user_id'])
    
    user5 = user_signup_info5()
    u_id5 = user_signup(user5) 
    u_id5['user_id'] = decode_id_frontend(u_id5['user_id'])
    u_id5['user_id'] = encode_id_frontend(u_id5['user_id'])  
      

    user_add_balance(u_id1['user_id'], 10000, u_id1['token'])
    user_add_balance(u_id2['user_id'], 10000, u_id2['token'])
    user_add_balance(u_id3['user_id'], 10000, u_id3['token'])
    user_add_balance(u_id4['user_id'], 10000, u_id4['token'])
    user_add_balance(u_id5['user_id'], 10000, u_id5['token']) 
    
    user_book_activity(a_id1, u_id1['user_id'], 1, 1, u_id1['token'])
    user_book_activity(a_id2, u_id1['user_id'], 1, 1, u_id1['token'])
    user_book_activity(a_id1, u_id2['user_id'], 12, 12, u_id2['token'])
    user_book_activity(a_id3, u_id3['user_id'], 11, 11, u_id3['token'])
    user_book_activity(a_id2, u_id4['user_id'], 2, 2, u_id4['token'])
    user_book_activity(a_id1, u_id4['user_id'], 3, 3, u_id4['token'])
    user_book_activity(a_id2, u_id5['user_id'], 3, 3, u_id5['token'])
    user_book_activity(a_id1, u_id5['user_id'], 4, 4, u_id5['token'])
    user_book_activity(a_id3, u_id5['user_id'], 2, 2, u_id5['token'])
    
    time_push_now({'week': 4, 'day': 4, 'time': 0})
    
    
    addCommit(u_id1['token'],None, u_id1['user_id'], 'Adding new message', a_id1, 2)
    addCommit(u_id1['token'],None, u_id1['user_id'], 'Adding new message', a_id2, 4)
    addCommit(u_id2['token'],None, u_id2['user_id'], 'Adding new message', a_id1, 3)
    addCommit(u_id3['token'],None, u_id3['user_id'], 'Adding new message', a_id3, 1)   
    addCommit(u_id4['token'],None, u_id4['user_id'], 'Adding new message', a_id2, 7)  
    addCommit(u_id4['token'],None, u_id4['user_id'], 'Adding new message', a_id1, 3)      
    
    addCommit(u_id5['token'],None,  u_id5['user_id'], 'Adding new message', a_id2, 7)    
    
    addCommit(u_id5['token'],None,  u_id5['user_id'], 'Adding new message', a_id1, 4) 
    
    addCommit(u_id5['token'],None,  u_id5['user_id'], 'Adding new message', a_id3, 1) 

    # return  a_id1, a_id2,a_id3, u_id1, u_id2, u_id3, u_id4,u_id5 
    return u_id1, a_id1
    


def test_user_recommend(basic_info):
    
    #a_id1, a_id2,a_id3, u_id1, u_id2, u_id3, u_id4,u_id5 = basic_info
    u_id1,aid = basic_info
    data = user_get_recommended(u_id1['user_id'], u_id1['token'])
    assert(data['activities_info'][0]['act_id'] == 3)  
    
    
def test_user_popular(basic_info):
    
    u_id1 = basic_info
    data = acts_get_popular()
    assert(data['activities_info'][0]['id'] == 1)
    assert(data['activities_info'][1]['id'] == 2)
    assert(data['activities_info'][2]['id'] == 3)
    
    
def test_time_begin():
    date = "2022-09-27 18:05:44"
    time_set_now(date)
    time_set = time_get_now()
    time_set2 = time_set['time']
    assert(str(time_set2) == date)
    push = {
      'week': 1,
      'day': 1,
      'hour': 1,
    }
    time_now = time_push_now(push)['time']
    assert(str(time_now) == '2022-10-05 19:05:44')

def test_host_name():
    clear_v1()
    date = "2022-09-27 18:05:44"
    time_set_now(date)
    login = host_signup('422922280@qq.com', '123123')
    login['host_id'] = decode_id_frontend(login['host_id'])
    login['host_id'] = encode_id_frontend(login['host_id'])    
    print(login['host_id'])  
    name = get_host_email_server(login['host_id'])
    assert(name['name'] == "422922280@qq.com")   


def test_user_name():
    clear_v1()
    date = "2022-09-27 18:05:44"
    time_set_now(date)
    user1 = user_signup_info()
    u_id1 = user_signup(user1) 
    u_id1['user_id'] = decode_id_frontend(u_id1['user_id'])
    u_id1['user_id'] = encode_id_frontend(u_id1['user_id'])  
    
    name = get_user_name_server(u_id1['user_id'])
    assert(name['name'] == "andy, wang")
    
 
def test_time_compare():
    clear_v1()
    date = "2022-09-27 18:05:44"
    time_set_now(date)
    a = time_after_now("2022-09-28")

    assert(a == True)
    
    
def test_listseat(basic_info):

    u1, a_id1 = basic_info
    data = list_seat(a_id1)

    assert(data == [{'id': 1, 'seat_x': 1, 'seat_y': 1}, {'id': 2, 'seat_x': 3, 'seat_y': 3},\
        {'id': 3, 'seat_x': 4, 'seat_y': 4}, {'id': 4, 'seat_x': 12, 'seat_y': 12}])

def test_overall_info(basic_info):
    u1, a_id1 = basic_info
    data = overall_information()
    print(data)
    assert(data == [{'name': 'number_of_user', 'value': 5}, {'name': 'number_of_host', 'value': 1}, \
        {'name': 'number_of_act', 'value': 4}, {'name': 'number_of_commit', 'value': 9}, \
        {'name': 'number_of_order', 'value': 9}, {'name': 'number_of_money', 'value': 1800.0}, \
        {'name': 'list_of_act', 'value': [{'id': 1, 'name': 'andy', 'description': 'aaa', \
        'sell_ticket': 4, 'ticket_money': 200.0, 'overall_money': 800.0}, {'id': 2, 'name':\
        'andy', 'description': 'aaa', 'sell_ticket': 3, 'ticket_money': 200.0, \
        'overall_money': 600.0}, {'id': 3, 'name': 'andy', 'description': 'aaa',\
        'sell_ticket': 2, 'ticket_money': 200.0, 'overall_money': 400.0},\
        {'id': 4, 'name': 'andy', 'description': 'aaa', 'sell_ticket': 0, 'ticket_money': \
        200.0, 'overall_money': 0.0}]}])

def test_overall_info(basic_info):
    u_id1, a_id1 = basic_info
    data = clear_token()
    u_id1['user_id']= decode_id_frontend(u_id1['user_id'])
    u_id1['user_id']= encode_id_frontend(u_id1['user_id'])
    token = dm.is_active_uid(u_id1['user_id'])
    assert(token == False)
    
