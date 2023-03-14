import pytest
from Activity import *
from ListActs import *
from data_sql import dm
from other import *
from host import *
from timeset import time_get_now, time_push_now, time_set_now
from user import *
from test_accounts import *
from act_recommend import *

def test_basic_info():
    clear_v1()
    date = "2018-07-21 18:05:44"    
    time_set_now(date)    
    
    login = host_signup('422922280@qq.com', '123123')
    login['host_id'] = decode_id_frontend(login['host_id'])
    login['host_id'] = encode_id_frontend(login['host_id'])    
    a_id1 = host_new_activity(login['host_id'], activity_create_info(login['host_id']), login['token'])
    a_id2 = host_new_activity(login['host_id'], activity_create_info2(login['host_id']), login['token']) 
    a_id3 = host_new_activity(login['host_id'], activity_create_info3(login['host_id']), login['token']) 
    a_id4 = host_new_activity(login['host_id'], activity_create_info4(login['host_id']), login['token'])    
    a_id5 = host_new_activity(login['host_id'], activity_create_info5(login['host_id']), login['token'])  
    a_id6 = host_new_activity(login['host_id'], activity_create_info6(login['host_id']), login['token'])
    a_id7 = host_new_activity(login['host_id'], activity_create_info7(login['host_id']), login['token'])
    a_id8 = host_new_activity(login['host_id'], activity_create_info(login['host_id']), login['token'])
    
    host_broadcast_notification(login['host_id'], a_id1, 'world', login['token'])
        
    user1 = user_signup_info()
    u_id1 = user_signup(user1) 
    u_id1['user_id'] = decode_id_frontend(u_id1['user_id'])
    u_id1['user_id'] = encode_id_frontend(u_id1['user_id'])
      
    result1 = get_description_recommended(u_id1['user_id'], u_id1['token'])
    
    assert(result1 == {'activities_info': []} )
    user_add_balance(u_id1['user_id'], 10000, u_id1['token'])

    
    user_book_activity(a_id1, u_id1['user_id'], 1, 1, u_id1['token'])
    user_book_activity(a_id2, u_id1['user_id'], 1, 1, u_id1['token'])
    user_book_activity(a_id3, u_id1['user_id'], 12, 12, u_id1['token'])
    user_book_activity(a_id4, u_id1['user_id'], 11, 11, u_id1['token'])
    
    # time_push_now({'week': 4, 'day': 4, 'time': 0})
    
    result = get_description_recommended(u_id1['user_id'], u_id1['token'])

    assert(len(result['activities_info']) == 4)
    user_logout(u_id1['user_id'], u_id1['token'])
    
