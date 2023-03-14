import pytest
from Activity import *
from ListActs import *
from data_sql import dm
from other import *
from host import *
from timeset import time_get_now, time_push_now, time_set_now
from user import *
from test_accounts import *
import pytest
from Activity import *
from ListActs import *
from data_sql import dm
from other import *
from host import *
from timeset import time_get_now, time_push_now, time_set_now
from user import *
from test_accounts import *

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
   
    
    # addCommit(u_id1['token'],None, u_id1['user_id'], 'Adding new message', a_id1, 2)

    user_logout(u_id1['user_id'], u_id1['token'])
    host_logout(login['host_id'],login['token'])


def test_init():
    clear_v1()
    date = "2022-9-21 18:05:44"    
    time_set_now(date)

    login_return = host_signup('host@163.com', 'Ab123456!')
    h_id = login_return["host_id"]
    h_id = decode_id_frontend(h_id)
    h_id1 = encode_id_frontend(h_id)
    h_token1 = login_return["token"]

    a_id1 = host_new_activity(h_id1, activity_create_init1(h_id1), h_token1)
    a_id4 = host_new_activity(h_id1, activity_create_init4(h_id1), h_token1)


    login_return = host_signup('host2@163.com', 'Ab123456!')
    h_id = login_return["host_id"]
    h_id = decode_id_frontend(h_id)
    h_id2 = encode_id_frontend(h_id)
    h_token2 = login_return["token"]

    a_id2 = host_new_activity(h_id2, activity_create_init2(h_id2), h_token2)


    login_return = host_signup('host3@163.com', 'Ab123456!')
    h_id = login_return["host_id"]
    h_id = decode_id_frontend(h_id)
    h_id3 = encode_id_frontend(h_id)
    h_token3 = login_return["token"]

    a_id3 = host_new_activity(h_id3, activity_create_init3(h_id3), h_token3)
    a_id33 = host_new_activity(h_id3, activity_create_init3(h_id3), h_token3)
    user = user_signup_init1()
    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id1 = encode_id_frontend(u_id)
    u_token1 = login_return["token"]

    user_add_balance(u_id1, 10000, u_token1)
    user_book_activity(a_id1, u_id1, 1, 1, u_token1)
    user_book_host(u_id1, h_id1, u_token1)

    user_book_activity(a_id2, u_id1, 1, 1, u_token1)
    user_book_host(u_id1, h_id2, u_token1)

    user_book_activity(a_id3, u_id1, 1, 1, u_token1)
    user_book_host(u_id1, h_id3, u_token1)
    

    
    user = user_signup_init2()
    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id2 = encode_id_frontend(u_id)
    u_token2 = login_return["token"]

    user_add_balance(u_id2, 10000, u_token2)
    user_book_activity(a_id1, u_id2, 2, 2, u_token2)
    user_book_host(u_id2, h_id3, u_token2)
    
    host_broadcast_notification(h_id1, a_id1, "Welcome to this act!", h_token1)
    a_id31 = host_new_activity(h_id3, activity_create_init31(h_id3), h_token3)

    date = "2022-11-14 18:05:44"    
    time_set_now(date)

    addCommit(u_token2, None, u_id2, 'Hello guys', a_id1 , 10)
    addCommit(u_token1, None, u_id1, 'Hello guys', a_id1 , 10)
    addCommit(u_token1, None, u_id1, 'Hello guys', a_id2 , 10)
    addCommit(u_token1, None, u_id1, 'Hello guys', a_id3 , 10)




    user = user_signup_init3()
    login_return = user_signup(user)
    u_id = login_return["user_id"]
    u_id = decode_id_frontend(u_id)
    u_id3 = encode_id_frontend(u_id)
    u_token3 = login_return["token"]
    user_logout(u_id3, u_token3)
    user_logout(u_id2, u_token2)
    user_logout(u_id1, u_token1)
    host_logout(h_id3, h_token3)
    host_logout(h_id2, h_token2)
    host_logout(h_id1, h_token1)


