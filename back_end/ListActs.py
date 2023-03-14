
from other import get_host_email
from data_sql import dm
from helper import *
from timeset import *
from act_recommend import *
from ListActs import *
from Activity import *
data_manager = dm
act_keys = ['id', 'hold_host', 'name', 'description', 'type', 'venue_name', 'venue_address', 'start_time', 'end_time', 'start_date', 'end_date', 'all_ticket',
            'possible_seats', 'ticket_money', 'seat_x', 'seat_y']


# When asking for listing all activities, if the host is online, then all activities created by the host
# would be listed according to the created order.
def host_list_activities(h_id, token):

    check_hid_token(h_id, token)
    h_id = decode_id_backend(h_id)

    if not data_manager.is_valid_hid(h_id):
        raise AccessError('invalid h_id')

    if not data_manager.is_active_hid(h_id):
        raise AccessError('not login')
    activities_info = []
    data1 = data_manager.get_act_info_by_hid(h_id)
    if data1 is None:
        data1 = ()
    count = 1
    for act in data1:

        #activities_info = [dict(zip(act_keys,i)) for i in data1]

        activity = tuple_act_to_list(act, (), ())
        if activity['name'] != 'DELETE ALREADY':

            activity['act_id'] = activity['id']
            activity['id'] = count
            activity['ticket_money'] = '$' + str(activity['ticket_money'])

            activities_info.append(activity)
            count = count + 1

    return {
        'activities_info': activities_info
    }


# When asking for listing all activities, if the user is online, then all activities the user joined in
# would be listed according to the order of joining.
def user_list_activities(u_id, token):

    check_uid_token(u_id, token)
    u_id = decode_id_backend(u_id)

    if not data_manager.is_valid_uid(u_id):
        raise AccessError('invalid u_id')
    if not data_manager.is_active_uid(u_id):
        raise AccessError('not login')
    user_all_activity_info = data_manager.get_all_activity_info_by_uid(u_id)
    if user_all_activity_info is None:
        user_all_activity_info = ()

    all_activitie_id = []

    for activity_info in user_all_activity_info:
        activity_id = activity_info[4]
        x = activity_info[1]
        y = activity_info[2]

        dictA = {
            "activity_id": activity_id,
            "seat_x": x,
            "seat_y": y,
            "booking_id": activity_info[0]

        }
        all_activitie_id.append(dictA)

    activities_info = []
    count = 1
    for activityloop in all_activitie_id:
        activity_id = activityloop['activity_id']
        act = data_manager.get_act_by_aid(activity_id)
        activity = tuple_act_to_list(act, (), ())
        activity['act_id'] = activity_id
        activity['id'] = count
        activity['ticket_money'] = '$' + str(activity['ticket_money'])
        activity['host_name'] = get_host_email(activity['hold_host'])['name']
        activity['seat_x'] = activityloop['seat_x']
        activity['seat_y'] = activityloop['seat_y']
        activity["booking_id"] = activityloop["booking_id"]

        activities_info.append(activity)

        count = count + 1

    return {
        'activities_info': activities_info
    }


# List all the activities to user
# It doesn't matter if user is in or not, list all
# It should return name, type, date, address and price
def listAll_activity(sort_by, kind):

    # set up a list for return value
    all_acts = []
    #check_uid_token(u_id, token)
    #u_id = decode_id_backend(u_id)
    # check if the u_id is valid or not

    now = time_get_now()['time']
    # if the result True: user exist
    # if the result False: user doesn't exist
    # if result is False:
    #     raise Exception('User does not exist')
    list_acts = data_manager.get_acts_by_sort(sort_by, kind)
    # list_acts = (
    #     (1, 'My Act', 'This is my act', 'music', 'Theatre', 'UNSW', None, None, 2020/2/2, 2020/2/4, 100, 100, 309, '', ''),
    #     (2, 'Hello World', 'C Python Java', 'music', 'Kingsford', 'USYD', None, None, 2020/2/2, 2020/2/4, 100, 100, 189, '', '')
    # )
    # list_acts is a tuple with couple tuples in it
    # loop through these acts to get informations we
    # need to show user
    if list_acts is None:
        list_acts = ()
    for acts in list_acts:
        if acts[1] != 'DELETE ALREADY':
            all_acts.append(tuple_act_to_list(acts, (), ()))

    if all_acts == []:
        return ['There is no activity recently']
    # return all the activities in list
    return all_acts


# List all the activities to user
# It doesn't matter if user is in or not, list all
# It should return name, type, date, address and price
def listAll_avaiable_activity():

    # set up a list for return value
    all_acts = []
    #check_uid_token(u_id, token)
    #u_id = decode_id_backend(u_id)
    # check if the u_id is valid or not

    now = time_get_now()['time']
    # if the result True: user exist
    # if the result False: user doesn't exist
    # if result is False:
    #     raise Exception('User does not exist')

    list_acts = data_manager.get_all_acts()
    # list_acts = (
    #     (1, 'My Act', 'This is my act', 'music', 'Theatre', 'UNSW', None, None, 2020/2/2, 2020/2/4, 100, 100, 309, '', ''),
    #     (2, 'Hello World', 'C Python Java', 'music', 'Kingsford', 'USYD', None, None, 2020/2/2, 2020/2/4, 100, 100, 189, '', '')
    # )
    # list_acts is a tuple with couple tuples in it
    # loop through these acts to get informations we
    # need to show user
    if list_acts is None:
        list_acts = ()

    for acts in list_acts:
        later = now + datetime.timedelta(days=30)
        start = datetime.datetime.combine(
            acts[9], (datetime.datetime.min + acts[7]).time())
        now_time = time_get_now()

        if later > start and start > now_time['time']:
            if acts[11] <= 0:
                continue

            if acts[1] != 'DELETE ALREADY':
                tuple_act = tuple_act_to_list(acts, (), ())
                tuple_act['host_name'] = get_host_email(
                    tuple_act['hold_host'])['name']
                all_acts.append(tuple_act)
    if all_acts == []:
        return ['There is no activity recently']
    # return all the activities in list
    return all_acts


# user recommend activity
def user_get_recommended(u_id, token):

    check_uid_token(u_id, token)
    u_id = decode_id_backend(u_id)
    all_activitie_id = get_list_act_by_recommended(u_id)
    find_act = []
    #  find user's all activity and get the recommended activity
    if all_activitie_id is None:
        all_activitie_id = ()
    count = 1
    new_list = []
    for i in all_activitie_id:
        if i not in new_list:
            new_list.append(i)
    for activity_id in new_list:
        activity = data_manager.get_act_by_aid(activity_id)
        activity = tuple_act_to_list(activity, (), ())
        activity['act_id'] = activity['id']
        activity['id'] = count
        activity['ticket_money'] = '$' + str(activity['ticket_money'])
        activity['host_name'] = get_host_email(activity['hold_host'])['name']
        find_act.append(activity)
        count = count + 1

    return {
        'activities_info': find_act
    }


# the most popular activity
def acts_get_popular():

    tuple = dm.get_most_popular_activities()
    if tuple is None:
        tuple = ()
    activities_info = []

    aidlist = []
    for act in tuple:
        activity1 = tuple_act_to_list(act, (), ())
        # if activity is delect, don't show it
        if activity1['name'] != 'DELETE ALREADY':
            aid = activity1['id']
            if aid not in aidlist:
                aidlist.append(aid)

    count = 1
    # make a loop to show better for front end
    for everya_id in aidlist:
        acts = data_manager.get_act_by_aid(everya_id)
        activity = tuple_act_to_list(acts, (), ())
        if activity['name'] != 'DELETE ALREADY':
            activity['act_id'] = activity['id']
            activity['id'] = count
            activity['ticket_money'] = '$' + str(activity['ticket_money'])
            activity['host_name'] = get_host_email(
                activity['hold_host'])['name']
            activities_info.append(activity)
            count = count + 1

    return {
        'activities_info': activities_info
    }


# recommend activity by user's activity description
def get_description_recommended(u_id, token):
    check_uid_token(u_id, token)
    u_id = decode_id_backend(u_id)
    # get all user's activity
    user_all_activity_info = data_manager.get_all_activity_info_by_uid(u_id)
    if user_all_activity_info is None:
        user_all_activity_info = ()

    all_activitie_id = []
    all_activity = []
    for activity_info in user_all_activity_info:
        activity_id = activity_info[4]
        dictA = {
            "id": activity_id,
        }
        all_activitie_id.append(dictA)

    # our algorithm just need activity description and activity id
    booking_infor = []
    for activityloop in all_activitie_id:
        activity_id = activityloop['id']
        act = data_manager.get_act_by_aid(activity_id)
        activity = tuple_helper(act)
        booking_infor.append(activity)

    all_act1 = data_manager.get_all_acts()
    all_act = []
    for act in all_act1:
        all_act2 = tuple_helper(act)
        all_act.append(all_act2)
    other_act = []
    for i in all_act:
        if i not in booking_infor:
            other_act.append(i)
    # using the description to find the recommended activity
    top3_list = recommendation_top5(booking_infor, other_act)

    noagain = []
    for i in top3_list:
        if i not in noagain:
            noagain.append(i)

    count = 1
    for a_id in noagain:
        acts = data_manager.get_act_by_aid(a_id)
        activity = tuple_act_to_list(acts, (), ())
        # if activity is delect, don't show it
        if activity['name'] != 'DELETE ALREADY':
            activity['act_id'] = activity['id']
            activity['id'] = count
            activity['ticket_money'] = '$' + str(activity['ticket_money'])
            activity['host_name'] = get_host_email(
                activity['hold_host'])['name']
            all_activity.append(activity)
            count = count + 1
    return {
        'activities_info': all_activity
    }


# simple helper function to convert tuple to list
def tuple_helper(acts):
    result = {
        'id': acts[0],
        'description': acts[3],
    }
    return result
