import pytest
from helper import *
from Activity import *
from ListActs import *
from data_sql import dm
from other import clear_v1
from host import *
from user import *
from test_accounts import *



#######################################################
##                 Activity List                     ##
#######################################################

def test_act_list_user_ok():
    clear_v1()
    
    date = "2018-07-1 18:05:44"    
    time_set_now(date)
    
    """             
                    Host Sign up               
                                            """
    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))

    

    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])
    """            
                Adding new activity         
                                            """
    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])
    host_broadcast_notification(sign_up['host_id'], a_id, 'Add new message', sign_up['token'])
    host_broadcast_notification(sign_up['host_id'], a_id, 'Add second message', sign_up['token'])
    
    user = user_signup_info()
    u_id = user_signup(user)
    assert(type(u_id) == dict)

    
    u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    assert(type(u_id) == dict)

    """            
                Listing one activity        
                                            """
    activity = one_activity_detail(a_id)

    """                
                    Testing               
                                            """
    assert(type(activity) == dict)
    assert(activity['name'] == 'andy')
    assert(activity['description'] == 'This mucial is very nice, Jay Chou love it')
    assert(activity['type'] == 'music')

    with pytest.raises(Exception):
        assert(type(activity['ticket_price']) == 200)


def test_act_list_host_ok():
    clear_v1()
    
    date = "2018-07-1 18:05:44"    
    time_set_now(date)
    
    """             
                    Host Sign up               
                                            """
    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))



    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])
    """            
                Adding new activity         
                                            """
    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])
    host_broadcast_notification(sign_up['host_id'], a_id, 'Add new message', sign_up['token'])
    host_broadcast_notification(sign_up['host_id'], a_id, 'Add second message', sign_up['token'])
    
    # user = user_signup_info()
    # u_id = user_signup(user)
    # assert(type(u_id) == int)

    # #wrong password
    # with pytest.raises(Exception):
    #     user_login('111a@163.com', '112a')

    # u_id = user_login('111a@163.com', '111a@163.com')
    # u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    # u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    # assert(type(u_id) == dict)

    """            
                Listing one activity        
                                            """
    activity = one_activity_detail(a_id)

    """                
                    Testing               
                                            """
    assert(type(activity) == dict)
    assert(activity['name'] == 'andy')
    assert(activity['description'] == 'This mucial is very nice, Jay Chou love it')
    assert(activity['type'] == 'music')

    with pytest.raises(Exception):
        assert(type(activity['ticket_price']) == 200)


def test_act_list_invalid_aID():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    """             
                    Host Sign up               
                                            """
    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))



    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])
    """            
                Adding new activity         
                                            """
    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    user = user_signup_info()
    u_id = user_signup(user)
    assert(type(u_id) == dict)

    u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    assert(type(u_id) == dict)

    """            
                Listing one activity        
                                            """
    activity = one_activity_detail(a_id)

    """                
                    Testing               
                                            """
    with pytest.raises(Exception):
        activity = one_activity_detail(sign_up['token'], sign_up['host_id'], a_id + 1)

#######################################################
##              Activity List All                    ##
#######################################################
def test_act_listAll_ok():

    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    """             
                    Host Sign up               
                                            """
    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))

    """             
                    Host Sign up               
                                            """
    sign_up1 = host_signup('1130333333@qq.com', '123321')
    assert(type(sign_up == int))

    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])
    sign_up1['host_id'] = decode_id_frontend(sign_up1['host_id'])
    sign_up1['host_id'] = encode_id_frontend(sign_up1['host_id'])
    """            
                Adding new activity         
                                            """
    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])
    a_id1 = host_new_activity(sign_up1['host_id'], activity_create_info(sign_up1['host_id']), sign_up1['token'])

    user = user_signup_info()
    u_id = user_signup(user)
    assert(type(u_id) == dict)

    u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    assert(type(u_id) == dict)
    """            
                Listing all activities       
                                            """
    activities = listAll_activity('type', 1)

    assert(type(activities) == list)
    assert(activities[0]['name'] == 'andy')
    assert(activities[1]['name'] == 'andy')
    assert(activities[0]['type'] == 'music')
    assert(activities[1]['type'] == 'music')

def test_act_listAll_avaiable_ok():

    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    """             
                    Host Sign up               
                                            """
    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))

    """             
                    Host Sign up               
                                            """
    sign_up1 = host_signup('1130333333@qq.com', '123321')
    assert(type(sign_up == int))


    

    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])
   

    sign_up1['host_id'] = decode_id_frontend(sign_up1['host_id'])
    sign_up1['host_id'] = encode_id_frontend(sign_up1['host_id'])
    """            
                Adding new activity         
                                            """
    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])
    a_id1 = host_new_activity(sign_up1['host_id'], activity_create_info(sign_up1['host_id']), sign_up1['token'])

    user = user_signup_info()
    u_id = user_signup(user)
    assert(type(u_id) == dict)

    
    u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    assert(type(u_id) == dict)
    """            
                Listing all activities       
                                            """
    activities = listAll_avaiable_activity()

    assert(type(activities) == list)
    assert(activities == ['There is no activity recently'])

#######################################################
##                Activity Search                    ##
#######################################################

def test_searchArc_ok():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))

    sign_up1 = host_signup('1130333333@qq.com', '123321')
    assert(type(sign_up == int))

    

    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])


    sign_up1['host_id'] = decode_id_frontend(sign_up1['host_id'])
    sign_up1['host_id'] = encode_id_frontend(sign_up1['host_id'])

    info = user_signup_info()
    user = user_signup(info)
    assert(type(user) == dict)


    user['user_id'] = decode_id_frontend(user['user_id'])
    user['user_id'] = encode_id_frontend(user['user_id'])
    assert(type(user) == dict)
    
    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])
    a_id1 = host_new_activity(sign_up1['host_id'], activity_create_info(sign_up1['host_id']), sign_up1['token'])

    activities = searchAct('and','','')

    assert(type(activities) == list)
    assert(activities[0]['name'] == 'andy')
    assert(activities[0]['type'] == 'music')


#######################################################
##              Activity User Commit                 ##
#######################################################

def test_addUserCommit_ok():

    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)


    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))

    

    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    user = user_signup_info()
    u_id = user_signup(user)
    assert(type(u_id) == dict)


    u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    assert(type(u_id) == dict)

    user_add_balance(u_id['user_id'], 1000, u_id['token'])
    user_book_activity(a_id, u_id['user_id'], 1, 1, u_id['token'])
    
    push = {
        'week': 5,
        'day' : 1,
        'time' : 1,
    }
    timestamp = time_push_now(push)['time']
    add = addCommit(u_id['token'], None, u_id['user_id'], 'Adding noram', a_id, 6)

    assert(type(add) == dict)
    assert(add['c_id'] == 1)



def test_addUserCommit_invalid_id():

    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))


    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    user = user_signup_info()
    u_id = user_signup(user)
    assert(type(u_id) == dict)


    u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    assert(type(u_id) == dict)

    user_add_balance(u_id['user_id'], 1000, u_id['token'])
    user_book_activity(a_id, u_id['user_id'], 1, 1, u_id['token'])
    with pytest.raises(Exception):
        add = addCommit(u_id['token'], None, 2, 'Adding new message', a_id, 6)

def test_addUserCommit_no_login():

    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))


    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    user = user_signup_info()
    u_id = user_signup(user)
    assert(type(u_id) == dict)

    # #wrong password
    # with pytest.raises(Exception):
    #     user_login('111a@163.com', '112a')
    #     u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    #     u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    #     user_add_balance(u_id['user_id'], 1000, u_id['token'])
    #     #user_add_balance(u_id, 1000)
    #     user_book_activity(a_id, u_id['user_id'], 1, 1, u_id['token'])
    #     #with pytest.raises(Exception):
    #     add = addUserCommit(u_id['token'], u_id['user_id'], 'Adding new message', a_id, 6)
    #     #u_id = user_login('111a@163.com', '111a@163.com')

    

def test_addUserCommit_not_inAct():

    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))


    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    user = user_signup_info()
    u_id = user_signup(user)
    assert(type(u_id) == dict)


    u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    assert(type(u_id) == dict)

    #user_book_activity(a_id, u_id, 1, 1)
    with pytest.raises(Exception):
        add = addCommit(u_id['token'], None, u_id['user_id'], 'Adding new message', a_id , 6)

def test_editUserCommit_ok():

    clear_v1()


    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))


    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    user = user_signup_info()
    u_id = user_signup(user)
    assert(type(u_id) == dict)

    
    u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    assert(type(u_id) == dict)

    user_add_balance(u_id['user_id'], 1000, u_id['token'])
    user_book_activity(a_id, u_id['user_id'], 1, 1, u_id['token'])
    
    push = {
        'week': 5,
        'day' : 1,
        'time' : 1,
    }
    timestamp = time_push_now(push)['time']
    
    add = addCommit(u_id['token'], None, u_id['user_id'], 'Adding new message', a_id, 6)

    assert(type(add) == dict)
    assert(add['c_id'] == 1)

    edit = editCommit(u_id['token'], None, u_id['user_id'], 'Editing Fuck message', a_id, add['c_id'])
    
    assert(edit == True)


def test_removeUserCommit_ok():

    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))


    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    user = user_signup_info()
    u_id = user_signup(user)
    assert(type(u_id) == dict)

    u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    assert(type(u_id) == dict)

    user_add_balance(u_id['user_id'], 1000, u_id['token'])
    user_book_activity(a_id, u_id['user_id'], 1, 1, u_id['token'])
    
    push = {
        'week': 5,
        'day' : 1,
        'time' : 1,
    }
    timestamp = time_push_now(push)['time']
    
    add = addCommit(u_id['token'], None, u_id['user_id'], 'Adding new message', a_id, 6)

    assert(type(add) == dict)
    assert(add['c_id'] == 1)

    edit = editCommit(u_id['token'], None, u_id['user_id'], 'Editing new message', a_id, add['c_id'])
    assert(edit == True)

    remove = removeCommit(u_id['token'], None, u_id['user_id'], a_id, add['c_id'])
    assert(remove == True)


#######################################################
##             Activity Host commit                  ##
#######################################################

def test_addHostCommit_ok():

    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))

    
    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    add = addCommit(sign_up['token'], sign_up['host_id'], None, 'Adding bad word Fuck', a_id, None)

    assert(type(add) == dict)
    assert(add['c_id'] == 1)



def test_addHostCommit_invalid_id():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))


    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    with pytest.raises(Exception):
        add = addCommit(sign_up['token'], sign_up['host_id'] + 1, None, 'Adding new message', a_id)


def test_addHostCommit_no_login():

    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)
    #a_id = host_new_activity(activity_create_info(login['host_id']))

    with pytest.raises(Exception):
        a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])
        #add = addHostCommit(h_id, 'Adding new message', a_id)



def test_addHostCommit_not_inAct():

    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))

    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    with pytest.raises(Exception):
        add = addCommit(sign_up['token'], sign_up['host_id'] + 1, None, 'Adding new message', a_id)




def test_editHostCommit_ok():

    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))

    
    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    add = addCommit(sign_up['token'], sign_up['host_id'], None, 'Adding new message', a_id, None)

    assert(type(add) == dict)
    assert(add['c_id'] == 1)


    edit = editCommit(sign_up['token'], sign_up['host_id'], None, 'Editing new message', a_id, add['c_id'])
    
    assert(edit == True)


def test_removeHostCommit_ok():

    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))
    
    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    add = addCommit(sign_up['token'], sign_up['host_id'], None, 'Adding new message', a_id, None)

    assert(type(add) == dict)
    assert(add['c_id'] == 1)


    edit = editCommit(sign_up['token'], sign_up['host_id'], None, 'Editing new message', a_id, add['c_id'])
    assert(edit == True)

    remove = removeCommit(sign_up['token'], sign_up['host_id'], None, a_id, add['c_id'])
    assert(remove == True)


def test_listAll_commit_ok():

#     commits = list_all_commit(1)

#     print(commits)
#     assert(type(commits) == list)
#     assert(commits[0]['sender'] == 1)
#     assert(commits[1]['sender'] == 1)
#     assert(commits[0]['message'] == 'Hello Host how are you?')
#     assert(commits[1]['message'] == 'Hello user I am good!')
#     assert(commits[1]['reply'] == 1)
    pass

#######################################################
##             Activity User reply                   ##
#######################################################
def test_userReply_commit_ok():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))

    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    h_cid = addCommit(sign_up['token'], sign_up['host_id'], None, 'Hello, I am host', a_id, None)

    user = user_signup_info()
    u_id = user_signup(user)
    assert(type(u_id) == dict)

    u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    assert(type(u_id) == dict)

    user_add_balance(u_id['user_id'], 1000, u_id['token'])
    ################################
    user_book_activity(a_id, u_id['user_id'], 1, 1, u_id['token'])
    add = ReplyCommit(u_id['token'], None, u_id['user_id'], 'Hi host, i am user', a_id, h_cid['c_id'])

    assert(type(add) == dict)
    assert(add['c_id'] == 2)

def test_userReply_commit_invalid_uid():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))


    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    h_cid = addCommit(sign_up['token'], sign_up['host_id'], None, 'Hello, I am host', a_id, None)

    user = user_signup_info()
    u_id = user_signup(user)
    assert(type(u_id) == dict)


    u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    assert(type(u_id) == dict)

    user_add_balance(u_id['user_id'], 1000, u_id['token'])
    ################################
    user_book_activity(a_id, u_id['user_id'], 1, 1, u_id['token'])
    with pytest.raises(Exception):
        add = ReplyCommit(u_id['token'], None, u_id['user_id'] + 1, 'Hi host, i am user', a_id, h_cid['c_id'])

def test_userReply_commit_invalid_aid():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))


    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    h_cid = addCommit(sign_up['token'], sign_up['host_id'], None, 'Hello, I am host', a_id, None)

    user = user_signup_info()
    u_id = user_signup(user)
    assert(type(u_id) == dict)

    u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    assert(type(u_id) == dict)

    user_add_balance(u_id['user_id'], 1000, u_id['token'])
    ################################
    user_book_activity(a_id, u_id['user_id'], 1, 1, u_id['token'])
    with pytest.raises(Exception):
        add = ReplyCommit(u_id['token'], None, u_id['user_id'], 'Hi host, i am user', a_id + 1, h_cid['c_id'])

def test_userReply_commit_invalid_cid():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))


    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    h_cid = addCommit(sign_up['token'], sign_up['host_id'], None, 'Hello, I am host', a_id, None)

    user = user_signup_info()
    u_id = user_signup(user)
    assert(type(u_id) == dict)


    u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    assert(type(u_id) == dict)

    user_add_balance(u_id['user_id'], 1000, u_id['token'])
    ################################
    user_book_activity(a_id, u_id['user_id'], 1, 1, u_id['token'])
    with pytest.raises(Exception):
        add = ReplyCommit(u_id['token'], None, u_id['user_id'], 'Hi host, i am user', a_id, h_cid['c_id'] + 1)

def test_userReply_commit_invalid_rating():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))


    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    h_cid = addCommit(sign_up['token'], sign_up['host_id'], None, 'Hello, I am host', a_id, None)

    user = user_signup_info()
    u_id = user_signup(user)
    assert(type(u_id) == dict)

    u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    assert(type(u_id) == dict)

    user_add_balance(u_id['user_id'], 1000, u_id['token'])
    ################################
    user_book_activity(a_id, u_id['user_id'], 1, 1, u_id['token'])
    with pytest.raises(Exception):
        add = ReplyCommit(u_id['token'], None, u_id['user_id'], 'Hi host, i am user', a_id, h_cid['c_id'] + 1)

def test_hostReply_commit_ok():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))

    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    h_cid = addCommit(sign_up['token'], sign_up['host_id'], None, 'Hello, I am host', a_id, None)

    user = user_signup_info()
    u_id = user_signup(user)
    assert(type(u_id) == dict)

    u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    assert(type(u_id) == dict)

    user_add_balance(u_id['user_id'], 1000, u_id['token'])
    user_book_activity(a_id, u_id['user_id'], 1, 1, u_id['token'])
    add = ReplyCommit(u_id['token'], None, u_id['user_id'], 'Hi host, i am user', a_id, h_cid['c_id'])

    assert(type(add) == dict)
    assert(add['c_id'] == 2)

    host_reply = ReplyCommit(sign_up['token'], sign_up['host_id'], None, 'Hey I see you!', a_id, add['c_id'])

    assert(type(add) == dict)
    assert(host_reply['c_id'] == 3)

def test_hostReply_commit_invalid_hid():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))

    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    h_cid = addCommit(sign_up['token'], sign_up['host_id'], None, 'Hello, I am host', a_id, None)

    user = user_signup_info()
    u_id = user_signup(user)
    assert(type(u_id) == dict)

    u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    assert(type(u_id) == dict)

    user_add_balance(u_id['user_id'], 1000, u_id['token'])
    user_book_activity(a_id, u_id['user_id'], 1, 1, u_id['token'])
    add = ReplyCommit(u_id['token'], None, u_id['user_id'], 'Hi host, i am user', a_id, h_cid['c_id'])

    assert(type(add) == dict)
    assert(add['c_id'] == 2)

    with pytest.raises(Exception):
        host_reply = ReplyCommit(sign_up['token'], sign_up['host_id'] + 1, None, 'Hey I see you!', a_id, add['c_id'])

def test_hostReply_commit_invalid_aid():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))


    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    h_cid = addCommit(sign_up['token'], sign_up['host_id'], None, 'Hello, I am host', a_id, None)

    user = user_signup_info()
    u_id = user_signup(user)
    assert(type(u_id) == dict)

    u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    assert(type(u_id) == dict)

    user_add_balance(u_id['user_id'], 1000, u_id['token'])
    user_book_activity(a_id, u_id['user_id'], 1, 1, u_id['token'])
    add = ReplyCommit(u_id['token'], None, u_id['user_id'], 'Hi host, i am user', a_id, h_cid['c_id'])

    assert(type(add) == dict)
    assert(add['c_id'] == 2)

    with pytest.raises(Exception):
        host_reply = ReplyCommit(sign_up['token'], sign_up['host_id'], None, 'Hey I see you!', a_id + 1, add['c_id'])

def test_hostReply_commit_invalid_cid():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))


    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    h_cid = addCommit(sign_up['token'], sign_up['host_id'], None, 'Hello, I am host', a_id, None)

    user = user_signup_info()
    u_id = user_signup(user)
    assert(type(u_id) == dict)

    u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    assert(type(u_id) == dict)

    user_add_balance(u_id['user_id'], 1000, u_id['token'])
    user_book_activity(a_id, u_id['user_id'], 1, 1, u_id['token'])
    add = ReplyCommit(u_id['token'], None, u_id['user_id'], 'Hi host, i am user', a_id, h_cid['c_id'])

    assert(type(add) == dict)
    assert(add['c_id'] == 2)

    with pytest.raises(Exception):
        host_reply = ReplyCommit(sign_up['token'], sign_up['host_id'], None, 'Hey I see you!', a_id, add['c_id'] + 2)



def test_reply_user_receive_ok():
    clear_v1()

    date = "2018-07-1 18:05:44"    
    time_set_now(date)

    sign_up = host_signup('422922280@qq.com', '123123')
    assert(type(sign_up == int))

    sign_up['host_id'] = decode_id_frontend(sign_up['host_id'])
    sign_up['host_id'] = encode_id_frontend(sign_up['host_id'])

    a_id = host_new_activity(sign_up['host_id'], activity_create_info(sign_up['host_id']), sign_up['token'])

    h_cid = addCommit(sign_up['token'], sign_up['host_id'], None, 'Hello, I am host', a_id, None)

    user = user_signup_info()
    u_id = user_signup(user)
    assert(type(u_id) == dict)

    u_id['user_id'] = decode_id_frontend(u_id['user_id'])
    u_id['user_id'] = encode_id_frontend(u_id['user_id'])
    assert(type(u_id) == dict)

    user_add_balance(u_id['user_id'], 1000, u_id['token'])
    user_book_activity(a_id, u_id['user_id'], 1, 1, u_id['token'])
    add = ReplyCommit(u_id['token'], None, u_id['user_id'], 'Hi host, i am user', a_id, h_cid['c_id'])

    assert(type(add) == dict)
    assert(add['c_id'] == 2)

    host_reply = ReplyCommit(sign_up['token'], sign_up['host_id'], None, 'Hey I see you!', a_id, add['c_id'])

    assert(type(add) == dict)
    assert(host_reply['c_id'] == 3)

    info = replyReceive(u_id['token'], None, u_id['user_id'],  3)

    assert(info == {})
    # assert(info['name'] == '422922280@qq.com')
    # assert(info['message'] == '422922280@qq.com: Hey I see you!')




