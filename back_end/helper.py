
import hashlib
from math import sqrt
from operator import le
from data_sql import dm
from recommended import RecommendationSystem
from error import *
from other import *

checkkey = ']]zl[]po\\12'
encodekey = {1: 9, 2: 4, 3: 2, 4: 7, 5: 3, 6: 8, 7: 1, 8: 6, 9: 5, 0: 0}
# def account_check_visa(account):
#
#     """
#     name:
#     limit time: not before now time
#     ACCOUNT NUMBER: 16 number
#     CSV: 3 number

#     """
#     # if account[1] < dm.get_timenow():
#     #     return False
#     if len(account[2]) != 16:
#         return False
#     for i in account[2]:
#         if i.is_digit() == False:
#             return False
#     if len(account[3]) != 3:
#         return False
#     for j in account[3]:
#         if j.is_digit() == False:
#             return False
#     return True


# def account_check_bpay(account):
#     """
#         BSB: 6 number
#         ACCOUNT NUMBER: 8 number
#         NAME: no limit
#     """
#     if len(account[0]) != 6:
#         return False
#     for i in account[0]:
#         if i.is_digit() == False:
#             return False
#     if len(account[1]) != 8:
#         return False
#     for i in account[1]:
#         if i.is_digit() == False:
#             return False
#     if len(account[2]) == 0:
#         return False
#     return True


def check_email(email):

    return
    # try:
    #     valid = validate_email(email)
    #     email = valid.email
    # except EmailNotValidError as e:
    #     raise  AccessError("Invalid email")

    # return


# encode password to make it cannot decode
def encode_password(password):
    message = hashlib.md5(password.encode('utf-8')).hexdigest()
    message = hashlib.md5(message.encode('gbk')).hexdigest()
    return message


def check_uid_token(id, token):
    # 1 uid decode
    #
    u_id = decode_id_backend(id)
    if int(u_id) < 0:
        raise AccessError("under 0")
    """
        check token get id ,
        id is same as input id
    """
    token = token.replace(" ", "+")
    check_num = dm.get_uid_by_token(token)

    if check_num is None:
        raise AccessError("Invalid token!!!!: %s" % check_num)
    if u_id != check_num:
        raise AccessError("not suitable token and id")
    """
    check id and token
    token is same as input token
    
    """
    if not dm.is_valid_uid(u_id):
        raise AccessError('invalid h_id')

    if not dm.is_active_uid(u_id):
        raise AccessError('not login')

    token_get = dm.get_token_by_uid(u_id)

    if token != token_get:
        raise AccessError("not suitable token and id")


def check_hid_token(id, token):
    # 1 hid decode
    #
    h_id = decode_id_backend(id)
    if int(h_id) < 0:
        raise AccessError("under 0")
    """
        check token get id ,
        id is same as input id
    """
    token = token.replace(" ", "+")
    check_num = dm.get_hid_by_token(token)

    if check_num is None:
        raise AccessError("Invalid token")
    print(check_num)
    print(h_id)
    if int(h_id) != int(check_num):
        raise AccessError("not suitable token and id")
    """
    check id and token
    token is same as input token
    
    """
    if not dm.is_valid_hid(h_id):
        raise AccessError('invalid h_id')

    if not dm.is_active_hid(h_id):
        raise AccessError('not login')

    token_get = dm.get_token_by_hid(h_id)
    if token != token_get:
        raise AccessError("not suitable token and id")


def encode_id_backend(id):
    # return id
    if type(id) == str:
        id = int(id)
    encoding = pow((id + 11), 2) + 9
    print(encoding)
    encoding = str(encoding)
    res = ''
    encoding = list(encoding)
    for i in range(0, len(encoding)):
        encoding[i] = str(encodekey[int(float(encoding[i]))])
    for i in range(0, len(encoding)):
        res = res + encoding[i]
    if type(res) == str:
        res = int(res)
    print(res)
    res = res * 2 + 29
    return res




def decode_id_backend(id):
    # return id
    if type(id) == str:
        id = int(id)
    decoding = id - 192
    decoding = str(decoding)
    decoding = list(decoding)
    print(decoding)
    for i in range(0, len(decoding)):
        if  decoding[i] == '1' and i == len(decoding) - 1 :
            decoding[i] = str(int(float(decoding[i]) - 1))
        elif decoding[i] == '1' and decoding[i+1] == '0':
            decoding[i] = '9'
            decoding[i + 1] = '-'
        elif decoding[i] == '-':
            continue
        else:
            decoding[i] = str(int(float(decoding[i]) - 1))
    res = ""
    print(decoding)
    for i in range(0, len(decoding)):
        if decoding[i] == '-':
            continue
        res = res + decoding[i]

    if type(res) == str:
        res = int(res)
    res = (res + 11)/18 - 20
    if res < 1:
        raise AccessError("Invalid id")
    if str(res).split('.')[1] == '0':
        res = int(res)
    else:
        raise AccessError("Invalid id")

    return res



def encode_id_frontend(id):
    # return id

    if type(id) == str:
        id = int(id)
    encoding = int((id + 20)*18 - 11)
    encoding = str(encoding)
    res = ''

    encoding = list(encoding)

    for i in range(0, len(encoding)):
        if encoding[i] == '9':
            encoding[i] = '10'
        else:
            # encoding = encoding.replace(str(i), str(i+1))

            encoding[i] = str(int(float(encoding[i]) + 1))
    for i in range(0, len(encoding)):
        res = res + encoding[i]

    if type(res) == str:
        res = int(res)
    res = res + 192
    return res


def decode_id_frontend(id):
    # return id
    if type(id) == str:
        id = int(id)
    decoding = int((id - 29)/2)
    print(decoding)
    decoding = str(decoding)
    res = ''
    decoding = list(decoding)
    for i in range(0, len(decoding)):
        j = int(float(decoding[i]))
        decoding[i] = str([k for k, v in encodekey.items() if v == j][0])

    for i in range(0, len(decoding)):
        res = res + decoding[i]

    if type(res) == str:
        res = int(res)
    res = (sqrt(res - 9) - 11)
    return res

    return id




def get_list_act_by_recommended(u_id):
    my_list = RecommendationSystem(u_id)
    list = my_list.find_rec()
    return list[0:5]


# Translate tuple from database to dictionary
def tuple_act_to_list(acts, notification, list_commit):

    notification_list = []
    # tuple to list, should notes that no need to change the order of the list
    all_commit = []
    if list_commit is not None:
        for commit in list_commit:
            all_commit.append(tuple_commit_to_list(commit))

    count = 1
    if notification is not None:
        for notice in notification:
            detail = {
                'id': count,
                'act_id': notice[1],
                'message': notice[2],
                'time': str(notice[3]),
            }
            notification_list.append(detail)
            count += 1

    # append this activity's info to the list
    result = {
        'id': acts[0],
        'hold_host': acts[1],
        'name': acts[2],
        'description': acts[3],
        'type': acts[4],
        'venue_name': acts[5],
        'venue_address': acts[6],
        'start_time': str(acts[7]),
        'end_time': str(acts[8]),
        'start_date': str(acts[9]),
        'end_date': str(acts[10]),
        'all_ticket': acts[11],
        'possible_seats': acts[12],
        'ticket_money': acts[13],
        'seat_x': acts[14],
        'seat_y': acts[15],
        'notification': notification_list,
        'image': acts[16],
        'commits': all_commit
    }

    # return all the activities in list
    return result


# Translate tuple from database to dictionary
def tuple_commit_to_list(commit):

    # translate the commits to list
    # be marked for user and host
    if commit[1] == None:
        sender_id = commit[2]
        sender_name = get_user_name(sender_id)['name']
        sender_type = 'user'
    else:
        sender_id = commit[1]
        sender_name = get_host_email(sender_id)['name']
        sender_type = 'host'
    result = {
        'commit_id': commit[0],
        'sender_type': sender_type,
        'sender_id': sender_id,
        'sender_name': sender_name,
        'message': commit[4],
        'time': str(commit[6]),
        'reply': commit[5],
        'rating': commit[7],
    }
    return result


def tuple_to_list_seat(seat, count):
    data = {
        'id': count,
        'seat_x': seat[1],
        'seat_y': seat[2]
    }
    return data


# a = ('1','2','3','4','5','6','7','8','9','10','11')
# act = {}
# keys = ['id','name','description','type','venue_name','venue_address','start_time','end_time','start_date','end_date','all_ticket',\
#     'possible_seats','ticket_money', 'seat_x', 'seat_y']
# # act["name"] = activity[2]
# # act["description"] = activity[3]
# # act["type"] = activity[4]
# # act["start_time"] = str(activity[7])
# # act["end_time"] = str(activity[8])
# # act["start_date"] = str(activity[9])
# # act["end_date"] = str(activity[10])
# act = dict(zip(keys,a))
# print(act)
