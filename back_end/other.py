from time import sleep
import helper


from data_sql import dm


def clear_v1():
    # clear all the data in the database
    dm.clear_data()
    dm.__init__()
    return


def get_user_name(user_id):
    # get user name by user id
    res = dm.get_user_by_uid(user_id)
    frist_name = res[3]
    last_name = res[4]
    name = frist_name + ", " + last_name
    name = {"name": name}
    return name

def get_user_name_server(user_id):
    # get user name by user id
    user_id = helper.decode_id_backend(user_id)
    res = dm.get_user_by_uid(user_id)
    frist_name = res[3]
    last_name = res[4]
    name = frist_name + ", " + last_name
    name = {"name": name}
    return name

def get_host_email_server(host_id):
    # get host email by host id for server
    host_id = helper.decode_id_backend(host_id)
    res = dm.get_host_by_hid(host_id)
    email = res[1]
    email = {"name": email}
    return email


def get_host_email(host_id):
    # get host email by host id for backend
    res = dm.get_host_by_hid(host_id)
    email = res[1]
    email = {"name": email}
    return email


def doing_check(n):
    sleep(n*0.01)


def clear_token():
    # clear all token for user and host
    dm.clear_token()
    return


def overall_information():
    # get overall information
    # showing as a pie chart
    number_of_user, number_of_host, number_of_act, number_of_commit, number_of_order = dm.get_all_info()
    acts = dm.get_sell_act()
    list_act = []
    number_of_money = 0
    for act in acts:
        actrecord = tuple_to_overall_acts(act)
        list_act.append(actrecord)
        number_of_money += actrecord['overall_money']
    res3 = change_to_model(list_act)

    res1 = [
        {
            'name': "User",
            'value': number_of_user if number_of_user != None else 0
        },
        {
            'name': "Host",
            'value': number_of_host if number_of_host != None else 0
        },
        {
            'name': "Act",
            'value': number_of_act if number_of_act != None else 0
        },
        {
            'name': "Comment",
            'value': number_of_commit if number_of_commit != None else 0
        },
        {
            'name': "Order",
            'value': number_of_order if number_of_order != None else 0
        },
        {
            'name': "Money",
            'value': number_of_money if number_of_money != None else 0
        }
    ]
    list_act = list_act if list_act != [] else [
        {'id': 'Null', 'name': 'Null', 'description': 'Null', 'sell_ticket': 0, 'ticket_money': 0, 'overall_money': 0}]
    res3 = res3 if res3 != [] else [{'name': 'Null', 'value': 0}]
    res = {
        'model1': res1,
        'model2': list_act,
        'model3': res3
    }
    return res


def tuple_to_overall_acts(act):

    result = {
        'id': act[0],
        'name': act[1],
        'description': act[2],
        'sell_ticket': act[3] - act[4],
        'ticket_money': act[5],
        'overall_money': (act[3] - act[4]) * act[5],
    }
    return result


def change_to_model(res1):
    res = []
    for i in res1:
        j = {}
        j['name'] = i['name']
        j['value'] = i['overall_money']
        res.append(j)
    return res
