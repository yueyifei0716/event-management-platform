from begin import *
from helper import *
from data_sql import dm
import datetime
from filter import *
from timeset import *
from error import *
from other import *
#import data_sql.is_valid_aid
# 判断 act里 发消息的 host是不是 act的创始者  check
# 每添加一个add 数据库就会有回值              check
# add 要返回一个 id message_id              check
# 当 发送新消息的时候 是否会返回一个id        check
# list all commit加一个 token 去判断 （待定）
# 如果收到回复，告诉被回复那个人 谁回复他了 时间 和回复了什么     check
# 判断list all的 排序方法                     check
# 考虑 list 所有 下个月的 activities
# 下个月 距离现在 30天？
# List all commit 需要根据时间排序
# user 必须在活动之后才能评论
# 活动开始 时间 可以 存精准到小时
# addCommit 需要 login return token
# 需要增加评分
# Reply 不需要 rating

#######################################################
##                  Helper Function                  ##
#######################################################

data_manager = dm
word_warehouse = ['Fuck', 'fuck', 'FUCK', 'bitch', 'Bitch', 'BITCH', 'ass', 'Ass', 'ASS',
                  'damn', 'Damn', 'DAMN', 'asshole', 'Asshole', 'ASSHOLE', 'goddam', 'Goddam', 'GODDAM',
                  'bullshit', 'Bullshit', 'BUllSHIT', 'Cock', 'Cock', 'COCK', 'dick', 'Dick', 'DICK',
                  'dickhead', 'Dickhead', 'DICKHEAD', 'motherfucker', 'Motherfucker', 'MOTHERFUCKER']
dfa = DFAUtils(word_warehouse=word_warehouse)

# # Translate tuple from database to dictionary


#######################################################
##                    Activity                       ##
#######################################################

# List one activity with name with it
# It should return name, type, date, address and price
# @param id int activity id
def one_activity_detail(a_id):
    # # check if the u_id is valid or not
    # To check if the activity exist or not
    print(a_id)
    if not data_manager.is_valid_aid(a_id):
        raise InputError('Activity does not exist')

    #acts = ((1, 'My Act', 'This is my act', 'music', 'Theatre', 'UNSW', datetime.timedelta(minutes=30), datetime.timedelta(minutes=30), 2020/2/2, 2020/2/4, 100, 100, 309, '', ''),)
    # if the activity exist, get information of the act
    acts = data_manager.get_act_by_aid(a_id)
    notification = data_manager.get_act_notification_by_aid(a_id)

    list_commit = data_manager.get_commit_in_act(a_id)
    if list_commit == None:
        list_commit = []
    return_record = tuple_act_to_list(acts, notification, list_commit)
    return_record['host_name'] = get_host_email(
        return_record['hold_host'])['name']

    # return dict with information of this act

    return return_record


# users can search activities by entering
# activity part name, full name, description and type
def searchAct(name, description, type):

    # set up a list for return value
    all_acts = []
    # Check if the activity exist
    list_act1 = []
    list_act2 = []
    list_act3 = []
    if name != '':
        list_act1 = data_manager.list_all_match_act('name', name)
    else:
        list_act1 = data_manager.get_all_acts()
    if description != '':
        list_act2 = data_manager.list_all_match_act('description', description)
    else:
        list_act2 = data_manager.get_all_acts()
    if type != '':
        list_act3 = data_manager.list_all_match_act('type', type)
    else:
        list_act3 = data_manager.get_all_acts()

    list_acts = list(set(list_act1) & set(list_act2) & set(list_act3))

    # if there is nothing in the result
    # it means no activity was found
    if list_acts == None:
        return all_acts
    else:
        for i in list_acts:
            all_acts.append(tuple_act_to_list(i, (), ()))

    return all_acts


def list_seat(a_id):
    # list all seat is be booked
    if type(a_id) != int:
        a_id = int(a_id)
    if not data_manager.is_valid_aid(a_id):
        raise InputError('Activity does not exist')
    data = data_manager.list_booking_seat(a_id)
    count = 1
    listres = []
    for i in data:
        listres.append(tuple_to_list_seat(i, count))
        count += 1
    return listres


# List all the commit in the activity
# @param a_id Activity id
def list_all_commit(a_id):

    # Set a list for all the commits in the activity
    all_commit = []

    # Check if the activity exist or not
    if not data_manager.is_valid_aid(a_id):
        raise AccessError('invalid a_id')
    list_commit = data_manager.get_commit_in_act(a_id)
    if list_commit == None:
        list_commit = []
    for commit in list_commit:
        all_commit.append(tuple_commit_to_list(commit))
    return all_commit


# User want to add commit to the activity
# @param a_id Activity id
# @param message    message user want to send
def addCommit(token, h_id, u_id, message, a_id, rating):

    if not data_manager.is_valid_aid(a_id):
        raise InputError('Activity does not exist')

    if h_id is None:
        # Check if the user exist or not
        check_uid_token(u_id, token)

        u_id = decode_id_backend(u_id)


        # To check if the user in the activity or not
        if not data_manager.is_user_in_act(a_id, u_id):
            raise AccessError('User has not joined the activity yet')

        # To check if the user has already commit in the act
        if data_manager.is_have_commit(u_id, a_id):
            raise InputError('User has already commit in the activity')
    else:
        # Check if the host exist or not
        check_hid_token(h_id, token)
        # # if the result True: host exist
        # # if the result False: host doesn't exist
        h_id = decode_id_backend(h_id)

        # Check if the activity made by the host
        if not data_manager.is_host_in_act(a_id, h_id):
            raise AccessError('Host is not part of the activity')

    timestamp = time_get_now()['time']
    # 对比时间
    act = data_manager.get_act_by_aid(a_id)

    start = datetime.datetime.combine(
        act[10], (datetime.datetime.min + act[8]).time())

    # if timestamp > start:
    if dfa.is_contain(message):
        message = dfa.replace_match_word(message)
    if h_id is None:
        if timestamp > start:
            commit = {
                'u_id': u_id,
                'act_id': a_id,
                'message': message,
                'reply_id': 0,
                'time': timestamp,
                'rating': rating,
            }
            commit_id = data_manager.add_commit_user(commit)
        else:
            raise InputError('Activity is not over yet')
    else:
        commit = {
            'h_id': h_id,
            'act_id': a_id,
            'message': message,
            'reply_id': 0,
            'time': timestamp,
        }
        # Add the message in activity's commit
        commit_id = data_manager.add_commit_host(commit)

    return {
        'c_id': commit_id
    }


# only can change message
def editCommit(token, h_id, u_id, message, a_id, c_id):
    if not data_manager.is_valid_aid(a_id):
        raise InputError('Activity does not exist')

    if not data_manager.is_valid_cid(c_id):
        raise AccessError('There is no such commit')

    if h_id is None:
        # Check if the user exist or not
        check_uid_token(u_id, token)
        u_id = decode_id_backend(u_id)
        # Maybe check if the act exist or not
        # To check if the user in the activity or not
        if not data_manager.is_user_in_act(a_id, u_id):
            raise AccessError('User has not joined the activity yet')

        # To check if the user has already commit in the act
        if not data_manager.is_have_commit(u_id, a_id):
            raise InputError('User has not  commit in the activity')

        commit = data_manager.get_commit_by_cid(c_id)

        if commit[2] != u_id:
            raise InputError('You do not have authority to edit this commit')

    else:
        # Check if the user exist or not
        check_hid_token(h_id, token)
        h_id = decode_id_backend(h_id)

        # Maybe check if the act exist or not

        # To check if the host in the activity or not
        if not data_manager.is_host_in_act(a_id, h_id):
            raise AccessError('Host is not part of the activity')

        commit = data_manager.get_commit_by_cid(c_id)

        if commit[1] != h_id:
            raise InputError('You do not have authority to edit this commit')

    if dfa.is_contain(message):
        message = dfa.replace_match_word(message)
    data_manager.edit_commit(c_id, message)
    commit = data_manager.get_commit_by_cid(c_id)
    if commit[4] == message:
        return True
    return False


def removeCommit(token, h_id, u_id, a_id, c_id):

    if not data_manager.is_valid_aid(a_id):
        raise InputError('Activity does not exist')

    # Maybe check if the act exist or not
    if not data_manager.is_valid_cid(c_id):
        raise AccessError('There is no such commit')

    if h_id is None:
        # Check if the user exist or not
        check_uid_token(u_id, token)
        u_id = decode_id_backend(u_id)

        # To check if the user in the activity or not
        if not data_manager.is_user_in_act(a_id, u_id):
            raise AccessError('User has not joined the activity yet')

        # To check if the user has already commit in the act
        if not data_manager.is_have_commit(u_id, a_id):
            raise InputError('User has not  commit in the activity')

        commit = data_manager.get_commit_by_cid(c_id)

        if commit[2] != u_id:
            raise AccessError(
                'You do not have authority to remove this commit')
    else:
        # Check if the host exist or not
        check_hid_token(h_id, token)
        h_id = decode_id_backend(h_id)

        # To check if the user in the activity or not
        if not data_manager.is_host_in_act(a_id, h_id):
            raise AccessError('User has not joined the activity yet')

        commit = data_manager.get_commit_by_cid(c_id)

        if commit[1] != h_id:
            raise AccessError(
                'You do not have authority to remove this commit')

    data_manager.remove_commit(c_id)

    commit = data_manager.get_commit_by_cid(c_id)

    if commit[4] == 'DELETE ALREADY':
        return True

    return False


# User want to reply commit to the activity
# @param a_id Activity id
# @param message    message user want to send
def ReplyCommit(token, h_id, u_id, message, a_id, c_id):

    if not data_manager.is_valid_aid(a_id):
        raise InputError('Activity does not exist')

    # Check if the user exist or not
    timestamp = time_get_now()['time']
    if h_id is None:
        check_uid_token(u_id, token)
        u_id = decode_id_backend(u_id)

        if not data_manager.is_valid_cid(c_id):
            raise AccessError('Commit does not exist')

        # Check if the activity exist or not
        if not data_manager.is_user_in_act(a_id, u_id):
            raise AccessError('User has not joined the activity yet')
        if dfa.is_contain(message):
            message = dfa.replace_match_word(message)

        commit = {
            'u_id': u_id,
            'act_id': a_id,
            'message': message,
            'reply_id': c_id,
            'time': timestamp,
            'rating': None,
        }
        commit_id = data_manager.add_commit_user(commit)
    else:
        check_hid_token(h_id, token)
        h_id = decode_id_backend(h_id)
        # Check if the activity exist or not

        if not data_manager.is_host_in_act(a_id, h_id):
            raise AccessError('Host is not part of the activity')

        if not data_manager.is_valid_cid(c_id):
            raise AccessError('This commit does not exist')

        if dfa.is_contain(message):
            message = dfa.replace_match_word(message)

        commit = {
            'h_id': h_id,
            'act_id': a_id,
            'message': message,
            'reply_id': c_id,
            'time': timestamp,
        }

        # Add the message in activity's commit
        commit_id = data_manager.add_commit_host(commit)

    # return the commit id
    return {
        'c_id': commit_id
    }


# Reply receive
# @param c_id commit_id user reply to
# It should return name, message, time
def replyReceive(token, h_id, u_id, c_id):

    # Check if the host exist or not
    # if the result True: host exist
    # if the result False: host doesn't exist
    if u_id is None:
        return {}

    check_uid_token(u_id, token)
    u_id = decode_id_backend(u_id)

    if not data_manager.is_valid_cid(c_id):
        raise AccessError('Commit does not exist')
    # Get detail of commit
    commit = data_manager.get_commit_by_cid(c_id)
    message = commit[4]
    message_time = commit[6]
    act_id = commit[3]
    # Check u_id and h_id
    # which one exist
    notification = {
        'u_id': u_id,
        'message': message,
        'time': str(message_time),
        'act_id': act_id,
    }
    n_id = data_manager.add_notifications(notification)

    return {}
