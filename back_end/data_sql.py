import base64
import functools
import json
import os
import random
import string
from time import sleep

import pymysql
from begin import *
import threading


def generate_token():
    """generate_token(): generate a new token for user in a new session
    @return (str): the new token"""
    return base64.b64encode(os.urandom(64)).decode("utf-8")


threadLock = threading.Lock()


class DataManager:

    def __init__(self):

        # try :
        #     db = pymysql.connect(host='localhost',
        #                         user='root',
        #                         password='0000',
        #                         database='mymyunsw')
        #     self.mycursor = db.cursor()
        # except Exception as err:
        #     self.mycursor = begin_db()

        qry = "CREATE DATABASE IF NOT EXISTS mymyunsw"
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='0000')
        # self.db = sqlite3.connect('mymyunsw.db')
        self.mycursor = self.db.cursor()
        self.mycursor.execute(qry)
        self.mycursor.execute("USE mymyunsw")
        self.mycursor = begin_db(self.mycursor)

    # USER

    def login_user(self, u_id):
        """login(u_id): login a user
        @param u_id(int): user id to log in
        @return (str): a new generated token for this session"""
        token = generate_token()
        token = self.db.escape_string(token)
        self.mycursor.execute(
            "UPDATE customers SET tokens = '%s' WHERE id = %d" % (token, u_id))
        self.commit_all()
        return token

    def logout_user(self, u_id):
        """logout(u_id): logout a user
        @param u_id(int): user id to log out
        @param token(str): token of this session
        @return (bool): whether successfully log out"""
        self.mycursor.execute(
            "UPDATE customers SET tokens = NULL WHERE id = %d" % (u_id))
        self.commit_all()

    def is_valid_uid(self, u_id):
        """is_valid_uid(u_id): checks user id existence
        @param u_id(int): user id to check upon
        @return (bool): if this user id is existent in the data manager
        @note: Caller must provide valid user Dict (see above)"""
        data = sql_select_sorting(
            self.db, self.mycursor, "customers", "id", u_id, None, None, None, 1)
        return (self.return_boolean(data) and data[0][3] != 'DELETE ALREADY')

    def is_active_uid(self, u_id):
        """is_active_uid(u_id): checks user id existence
        @param u_id(int): user id to check upon
        @return (bool): if this user id is active in the data manager """

        data = sql_select_sorting(
            self.db, self.mycursor, "customers", "id", u_id, None, None, None, 1)
        if data == ():
            return False
        return (data[0][8] != None)

    def get_token_by_uid(self, u_id):
        """get_token_by_uid(u_id): get token of a user
        @param u_id(int): user id to get token
        @return (str): token of this user"""

        data = sql_select_sorting(
            self.db, self.mycursor, "customers", "id", u_id, None, None, None, 1)
        if data == ():
            return None
        return data[0][8]

    def add_user(self, user):
        """add_user(user): adds user into data manager
        @param user(dict): user data blob whose format should conform to the
            regulations as described in [DataManager]
        @return (int): user id (a.k.a. uid) of the newly created user
        @note: this will not check for duplicating emails. you are advised to
            perform checks on your own."""
        for keys in user:
            user[keys] = self.db.escape_string(user[keys])
        qry = "INSERT INTO customers (email, password, name_first, name_last, address, bill_method, account, balance) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s','0')" % (
            user["email"], user["password"], user["name_first"], user["name_last"], user["address"], user["bill_method"], user["account"])
        self.mycursor.execute(qry)
        self.commit_all()
        return get_now_id("customers", self.mycursor)

    def edit_user(self, u_id, user):
        """edit_user(user): edits user in data manager
        @param u_id(int): user id to edit profile
        @param user(dict): user data blob whose format should conform to the
            regulations as described in [DataManager]
        @return (None)"""
        for keys in user:
            user[keys] = self.db.escape_string(user[keys])
        qry = "UPDATE customers SET email = '%s', name_first = '%s', name_last = '%s', address = '%s'  WHERE id = %d" % (
            user["email"], user["name_first"], user["name_last"], user["address"], u_id)
        self.mycursor.execute(qry)
        self.commit_all()

    def edit_user_password(self, u_id, password):
        """edit_user_password(u_id, password): edits user password in data manager
        @param u_id(int): user id to edit password
        @param password(str): new password
        @return (None)"""
        password = self.db.escape_string(password)
        self.mycursor.execute(
            "UPDATE customers SET password = '%s' WHERE id = %d" % (password, u_id))
        self.commit_all()

    def edit_user_payment(self, u_id, bill_method, account):
        """ edits user payment in data manager
        @param u_id(int): user id to edit payment
        @param bill_method(str): new bill_method
        @param account(str): new account
        @return (None)"""

        qry = "UPDATE customers SET bill_method = '%s', account = '%s'  WHERE id = %d" % (
            bill_method, account, u_id)
        self.mycursor.execute(qry)
        self.commit_all()

    def remove_user(self, u_id):
        """remove_user(user): removes user in data manager
        @param u_id(int): user id to remove
        @return (None)"""
        self.mycursor.execute(
            "UPDATE customers SET name_frist = 'DELETE ALREADY'AND email = 'DELETE ALREADY' WHERE id = %d", (u_id))
        self.commit_all()

    def get_uid_by_email(self, email):
        """get_uid_by_email(email): finds user id by email
        @param email(str): email address to look up
        @return (int/None): user id if such user matching the email exists,
            or None if such user does not exist"""
        data = sql_select_sorting(
            self.db, self.mycursor, "customers", "email", email, None, None, None, 1)
        return self.return_int(data)

    def get_uid_by_token(self, token):
        """get_uid_by_token(token): finds user id by token
        @param token(str): token to look up
        @return (int/None): user id if such user matching the token exists,
            or None if such token is invalid"""
        f = open("token.txt", "a")
        f.write(json.dumps(token))
        f.close()
        threadLock.acquire()
        # i = random.randint(0, 100)/100
        # if i > 0.5:
        #     i = i - 0.4
        # sleep(i)
        data = get_userbytoken(token, self.mycursor)
        data = self.return_int(data)
        threadLock.release()
        return data

    def get_user_by_uid(self, u_id):
        """get_user_by_uid(u_id): finds user by user id
        @param u_id(int): u_id to look up
        @return (dict/None): user if such user matching the user id exists,
            or None if such user id is invalid"""

        #
        #data = get_userbyid(u_id, self.mycursor)
        data = sql_select_sorting(
            self.db, self.mycursor, "customers", "id", u_id, None, None, None, 1)
        # threadLock.release()
        return self.return_record(data)

    def edit_balance_by_uid(self, u_id, balance):
        """edit_balance_by_uid(u_id, balance): edits user balance by user id
        @param u_id(int): u_id to look up
        @param balance(int): How much change in balance
        @return (None)"""

        # data = sql_select(self.mycursor, "customers", "id", u_id)
        data = sql_select_sorting(
            self.db, self.mycursor, "customers", "id", u_id, None, None, None, 1)
        balance_old = data[0][9]
        balance = balance_old + balance
        self.mycursor.execute(
            "UPDATE customers SET balance = %f WHERE id = %d" % (balance, u_id))
        self.commit_all()

    def is_enough_balance_by_uid(self, u_id, balance):
        """is_enough_balance_by_uid(u_id, balance): checks if user has enough balance by user id
        @param u_id(int): u_id to look up
        @param balance(float): How much balance in need
        @return (bool)"""
        data = sql_select_sorting(
            self.db, self.mycursor, "customers", "id", u_id, None, None, None, 1)
        money = data[0][9]
        if money >= balance:
            return True
        return False

    # HOST

    def login_host(self, h_id):
        """login(u_id): login a user
        @param u_id(int): user id to log in
        @return (str): a new generated token for this session"""
        token = generate_token()
        token = self.db.escape_string(token)
        self.mycursor.execute(
            "UPDATE hosts SET tokens = '%s' WHERE id = %d" % (token, h_id))
        self.commit_all()
        return token

    def logout_host(self, h_id):
        """logout(u_id): logout a user
        @param u_id(int): user id to log out
        @param token(str): token of this session
        @return (bool): whether successfully log out"""

        self.mycursor.execute(
            "UPDATE hosts SET tokens = NULL WHERE id = %d" % (h_id))
        self.commit_all()

    def is_valid_hid(self, h_id):
        """is_valid_uid(u_id): checks user id existence
        @param u_id(int): user id to check upon
        @return (bool): whether such user id exists"""
        data = sql_select_sorting(
            self.db, self.mycursor, "hosts", "id", h_id, None, None, None, 1)
        return self.return_boolean(data) and data[0][1] != 'DELETE ALREADY'

    def is_active_hid(self, h_id):
        """is_active_hid(h_id): Checks if host is active
        @param h_id(int): host id to check upon
        @return (bool): if this host id is active in the data manager"""
        data = sql_select_sorting(
            self.db, self.mycursor, "hosts", "id", h_id, None, None, None, 1)
        if data == ():
            return False
        return (data[0][3] != None)

    def get_token_by_hid(self, h_id):
        """ gets token by host id
        @param h_id(int): host id to look up
        @return (str/None): token if such host matching the host id exists,
            or None if such host id is invalid"""

        data = sql_select_sorting(
            self.db, self.mycursor, "hosts", "id", h_id, None, None, None, 1)
        if data == ():
            return None
        return data[0][3]

    def add_host(self, host):
        """add_user(user): adds user into data manager
        @param user(dict): user data blob whose format should conform to the
            regulations as described in [DataManager]
        @return (int): user id (a.k.a. uid) of the newly created user
        @note: this will not check for duplicating emails. you are advised to
            perform checks on your own."""
        for key in host:
            host[key] = self.db.escape_string(host[key])
        qry = "INSERT INTO hosts (email, password) VALUES ('%s', '%s')" % (
            host["email"], host["password"])
        self.mycursor.execute(qry)
        self.commit_all()
        return get_now_id("hosts", self.mycursor)

    def edit_host_password(self, h_id, password):
        """ edit_host_password(h_id, password): edits host password by host id
        @param h_id(int): h_id to look up
        @param password(str): new password
        @return (None)"""
        password = self.db.escape_string(password)
        self.mycursor.execute(
            "UPDATE hosts SET password = '%s' WHERE id = %d" % (password, h_id))
        self.commit_all()

    def remove_host(self, h_id):
        """remove_user(user): removes user in data manager
        @param u_id(int): user id to remove
        @return (None)"""
        qry = "UPDATE hosts SET email = 'DELETE ALREADY' WHERE id = %d", (h_id)
        self.mycursor.execute(qry)
        self.commit_all()

    def get_hid_by_email(self, email):
        """get_uid_by_email(email): finds user id by email
        @param email(str): email address to look up
        @return (int/None): user id if such user matching the email exists,
            or None if such user does not exist"""
        data = sql_select_sorting(
            self.db, self.mycursor, "hosts", "email", email, None, None, None, 1)
        return self.return_int(data)

    def get_hid_by_token(self, token):
        """get_uid_by_token(token): finds user id by token
        @param token(str): token to look up
        @return (int/None): user id if such user matching the token exists,
            or None if such token is invalid"""

        threadLock.acquire()

        data = sql_select_sorting(
            self.db, self.mycursor, "hosts", "tokens", token, None, None, None, 1)

        threadLock.release()
        return self.return_int(data)

    def get_host_by_hid(self, h_id):
        """get_user_by_uid(u_id): finds user by user id
        @param u_id(int): u_id to look up
        @return (dict/None): user if such user matching the user id exists,
            or None if such user id is invalid"""
        data = sql_select_sorting(
            self.db, self.mycursor, "hosts", "id", h_id, None, None, None, 1)
        return self.return_record(data)

    # act

    def is_valid_aid(self, act_id):
        """is_valid_act_id(act_id): checks act id existence
        @param act_id(int): act id to check upon
        @return (bool): if this act id is existent in the data manager """
        data = sql_select_sorting(
            self.db, self.mycursor, "acts", "id", act_id, None, None, None, 1)
        return self.return_boolean(data) and data[0][2] != 'DELETE ALREADY'

    def get_act_by_aid(self, act_id):
        """get_act_by_aid(act_id): find act by act id
        @param act_id(int): act id to look up
        @return (dict/None): act if such act matching the act id exists,
            or None if such act id is invalid"""
        data = sql_select_sorting(
            self.db, self.mycursor, "acts", "id", act_id, None, None, None, 1)
        return self.return_record(data)

    def is_host_in_act(self, act_id, h_id):
        """check_host_in_act(act_id, h_id): check if a host is in an act
        @param act_id(int): act id to look up
        @param h_id(int): host id to look up
        @return (bool): if such host is in the act"""
        data = sql_select_sorting(
            self.db, self.mycursor, "acts", "id", act_id, "hold_host", h_id, None, 1)
        return self.return_boolean(data)

    def is_user_in_act(self, act_id, u_id):
        """check_user_in_act(act_id, u_id): check if a user is in an act
        @param act_id(int): act id to look up
        @param u_id(int): user id to look up
        @return (bool): if such user is in the act"""
        data = sql_select_sorting(
            self.db, self.mycursor, "booking_information", "act_id", act_id, "u_id", u_id, None, 1)
        # print(data)
        return self.return_boolean(data)

    def get_commit_in_act(self, act_id):
        """get_commit_in_act(act_id): get the commit in an act
        @param act_id(int): act id to look up
        @return (int): the commit in the act"""
        data = sql_select_sorting(
            self.db, self.mycursor, "commits", "act_id", act_id, None, None, None, 1)
        return self.return_tuple(data)

    def add_act(self, act):
        """add_act(act): adds act into data manager
        @param act(dict): act data blob whose format should conform to the
            regulations as described in [DataManager]
        @return (int): act id (a.k.a. aid) of the newly created act """
        for keys in act:
            if type(act[keys]) is not string:
                continue
            act[keys] = self.db.escape_string(act[keys])

        qry = "INSERT INTO acts (hold_host, name, description, type, venue_name, venue_address, start_time, end_time, start_date, end_date, all_ticket, \
            possible_seats, ticket_money, seat_x, seat_y, image) VALUES (%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d, %d, '%s')" % (act["host_id"],
                                                                                                                                                                 act["name"], act["description"], act["type"], act["venue_name"], act[
                                                                                                                                                                     "venue_address"], act["start_time"], act["end_time"], act["start_date"],
                                                                                                                                                                 act["end_date"], act["all_ticket"], act["possible_seats"], act["ticket_money"], act["seat_x"], act["seat_y"], act["image"])

        self.mycursor.execute(qry)
        self.commit_all()
        return get_now_id("acts", self.mycursor)

    def remove_act(self, act_id):
        """ remove_act(act_id): removes act in data manager
        @param act_id(int): act id to remove
        @return (None)"""
        qry = "UPDATE acts SET name = 'DELETE ALREADY' WHERE id = %d" % (
            act_id)
        self.commit_all()
        self.mycursor.execute(qry)

    def is_seat_not_full_by_act_id(self, act_id, seat_x, seat_y):
        """is_seat_full_by_act_id(act_id): checks if the seat is full
        @param act_id(int): act id to check upon    
        @param seat_x(int): seat x to check upon
        @param seat_y(int): seat y to check upon
        @return (bool): if this seat is full in the act"""
        data = sql_select_sorting(
            self.db, self.mycursor, "booking_information", "x", seat_x, "y", seat_y, None, 1)
        # if data == ():
        #     return True
        for i in data:
            if i[4] == act_id:
                return False
        return True

    def add_user_to_act(self, a_id, u_id, seat_x, seat_y):
        """add_member_to_channel(c_id, u_id): adds member to a channel
        @param c_id(int): channel id to add to
        @param u_id(int): user id to add
        @return (None)"""
        qry = "INSERT INTO booking_information (act_id, u_id, x, y) VALUES (%d, %d, %d, %d)" % (
            a_id, u_id, seat_x, seat_y)
        self.mycursor.execute(qry)
        qry = "UPDATE acts SET possible_seats = possible_seats - 1 WHERE id = %d " % (
            a_id)
        self.mycursor.execute(qry)
        self.commit_all()
        return get_now_id("booking_information", self.mycursor)

    def remove_use_from_act(self, act_id, booking_id, u_id):
        """remove_member_to_channel(c_id, u_id): removes member from a channel
        @param c_id(int): channel id to remove from
        @param u_id(int): user id to remove
        @return (None)"""
        qry = "DELETE FROM booking_information WHERE act_id = %d AND u_id = %d And id = %d" % (
            act_id, u_id, booking_id)
        self.mycursor.execute(qry)
        qry = "UPDATE acts SET possible_seats = possible_seats + 1 WHERE id = %d" % (
            act_id)
        self.mycursor.execute(qry)
        self.commit_all()

    def remove_this_user_from_act(self, act_id, u_id):
        """remove_member_to_act(c_id, u_id): removes member from a act
        @param act_id(int): act id to remove from
        @param u_id(int): user id to remove
        @return (None)"""

        qry = "DELETE FROM booking_information WHERE act_id = %d AND u_id = %d " % (
            act_id, u_id)
        self.mycursor.execute(qry)
        qry = "UPDATE acts SET possible_seats = possible_seats + 1 WHERE id = %d" % (
            act_id)

        self.mycursor.execute(qry)
        self.commit_all()

    def list_all_users_by_act(self, act_id):
        """list_all_users(): lists all users in the data manager
        @param act_id(int): act id to look up
        @return (tuple): tuple of all users"""
        data = sql_select_sorting(
            self.db, self.mycursor, "booking_information", "act_id", act_id, None, None, None, 1)
        return self.return_tuple(data)

    def list_all_match_act(self, search, name):
        """list_all_match_act(search, name): lists all match act in the data manager
        @param search(str): search type
        @param name(str): search name
        @return (tuple): tuple of all match act"""
        data = sql_match(self.db, self.mycursor, "acts", search, name)
        return data

    def list_booking_seat(self, act_id):
        """list_booking_seat(act_id): lists all booking seat in the data manager
        @param act_id(int): act id to check upon
        @return (tuple): tuple of all booking seat"""
        qry = "SELECT * FROM booking_information WHERE act_id = %d Order by x,y ASC" % (
            act_id)
        self.mycursor.execute(qry)
        data = self.mycursor.fetchall()
        #data = sql_select_sorting(self.db, self.mycursor, "booking_information", "act_id", act_id, None, None, 'x', 1)
        return data

    # LIST ACTS

    def get_all_activity_info_by_uid(self, u_id):
        """get_channels_by_uid(u_id): finds user's channels by user id
        @param u_id(int): u_id to look up
        @return (tuple): a tuple of user's channels"""
        data = sql_select_sorting(
            self.db, self.mycursor, "booking_information", "u_id", u_id, None, None, None, 1)
        return self.return_tuple(data)

    def get_act_info_by_hid(self, h_id):
        """get_channels_by_hid(h_id): finds acts by host id
        @param h_id(int): h_id to look up
        @return (tuple): a tuple of act """
        data = sql_select_sorting(
            self.db, self.mycursor, "acts", "hold_host", h_id, None, None, None, 1)
        return self.return_tuple(data)

    def get_all_acts(self):
        """get_all_channels(): list all acts in the data manager
        @param (None)
        @return (tuple): a tuple of all acts"""
        data = sql_select_sorting(
            self.db, self.mycursor, "acts", None, None, None, None, "type", 1)
        return data

    # act in order

    def get_acts_by_sort(self, sort_by, kind):
        """get_channels_by_uid(u_id): finds user's channels by user id
        @param u_id(int): u_id to look up
        @return (tuple): a tuple of user's channels"""
        # data = sql_select_sort(self.mycursor, "acts", sort_by, kind)
        data = sql_select_sorting(
            self.db, self.mycursor, "acts", None, None, None, None, sort_by, kind)
        return self.return_tuple(data)

    # COMMIT

    def is_valid_cid(self, c_id):
        """is_valid_cid(c_id): checks if commit id is valid
        @param c_id(int): commit id to check
        @return (bool): True if valid, False if not"""
        data = sql_select_sorting(
            self.db, self.mycursor, "commits", "id", c_id, None, None, None, 1)
        return self.return_boolean(data) and data[0][4] != 'DELETE ALREADY'

    def is_have_commit(self, u_id, a_id):
        """is_have_commit(u_id, a_id): checks if this user have commit in this act
        @param u_id(int): user id to check upon
        @param a_id(int): act id to check upon
        @return (bool): if this user have commit in this act"""

        data = sql_select_sorting(
            self.db, self.mycursor, "commits", "u_id", u_id, "act_id", a_id, None, 1)
        return self.return_boolean(data)

    def add_commit_user(self, commit):
        """add_commit_user(commit): adds a commit to the data manager
        @param commit(Commit): commit to add
        @return (None)"""
        for keys in commit:
            if type(commit[keys]) != str:
                continue
            commit[keys] = self.db.escape_string(commit[keys])
        qry = "INSERT INTO commits (u_id, act_id, message, reply_id, time, rating) VALUES ( %d, %d, '%s', %d, '%s', '%s')" % (
            commit["u_id"], commit["act_id"], commit["message"], commit["reply_id"], commit["time"], commit["rating"])
        self.mycursor.execute(qry)
        self.commit_all()
        return get_now_id("commits", self.mycursor)

    def add_commit_host(self, commit):
        """add_commit_host(commit): adds a commit to the data manager
        @param commit(Commit): commit to add
        @return (None)"""
        for keys in commit:
            if type(commit[keys]) != str:
                continue
            commit[keys] = self.db.escape_string(commit[keys])

        qry = "INSERT INTO commits (h_id, act_id, message, reply_id, time) VALUES ( %d, %d, '%s', %d, '%s')" % (
            commit["h_id"], commit["act_id"], commit["message"], commit["reply_id"], commit["time"])
        self.mycursor.execute(qry)
        self.commit_all()
        return get_now_id("commits", self.mycursor)

    def edit_commit(self, c_id, content):
        """edit_commit(c_id, content): edits a commit in the data manager
        @param c_id(int): commit id to edit
        @param content(str): content to edit
        @return (None)"""
        content = self.db.escape_string(content)
        qry = "UPDATE commits SET message = '%s' WHERE id = %d" % (
            content, c_id)
        self.commit_all()
        self.mycursor.execute(qry)

    def remove_commit(self, c_id):
        """remove_commit(c_id): removes a commit from the data manager
        @param c_id(int): commit id to remove
        @return (None)"""
        qry = "UPDATE commits SET message = 'DELETE ALREADY' WHERE id = %s" % (
            c_id)
        self.commit_all()
        self.mycursor.execute(qry)

    # new updata
    # What is the content of the reply used to add to the notification message

    def get_commit_by_cid(self, c_id):
        """get_commit_by_cid(c_id): finds commit by commit id
        @param c_id(int): commit id to look up
        @return (tuple): a tuple of commit"""
        data = sql_select_sorting(
            self.db, self.mycursor, "commits", "id", c_id, None, None, None, 1)
        return self.return_record(data)

    # notifications

    # new updata
    # New read identifier added

    def add_notifications(self, notifications):
        """add a notification in data manager
        @param notifications(str): notifications content
        @return (int): new generated n_id"""
        notifications["message"] = self.db.escape_string(
            notifications["message"])
        qry = "INSERT INTO notifications (u_id, act_id, message, time, is_read) VALUES (%d, %d, '%s', '%s', FALSE)" % (
            notifications["u_id"], notifications["act_id"], notifications["message"], notifications["time"])

        self.mycursor.execute(qry)
        self.commit_all()
        return get_now_id("notifications", self.mycursor)

    def get_all_notifications_by_uid(self, u_id):
        """ get all notifications by user id
        @param u_id(int): user id to look up
        @return (tuple): a tuple of user's notifications"""

        data = sql_select_sorting(
            self.db, self.mycursor, "notifications", "u_id", u_id, None, None, None, 1)
        return self.return_tuple(data)

    def add_commit_notifications(self, notifications):
        """add a notification in data manager
        @param notifications(str): notifications content
        @return (int): new generated n_id"""
        notifications["message"] = self.db.escape_string(
            notifications["message"])
        qry = "INSERT INTO notifications (u_id,  message, time, is_read) VALUES (%d,  '%s', '%s', FALSE)" % (
            notifications["u_id"],  notifications["message"], notifications["time"])
        self.mycursor.execute(qry)
        self.commit_all()
        return get_now_id("notifications", self.mycursor)

    def is_user_notification(self, u_id, n_id):
        """is_user_notification(u_id, n_id): checks if user is the owner of the notification
        @param u_id(int): user id to look up
        @param n_id(int): notification id to look up
        @return (bool): True if user is the owner of the notification, False otherwise"""
        qry = "SELECT * FROM notifications WHERE u_id = %d AND id = %d" % (
            u_id, n_id)
        data = self.mycursor.execute(qry)
        return self.return_boolean(data)

    def delete_notification(self, n_id):
        """delete a notification in data manager
        @param n_id(int): notification id to delete
        @return (None)"""
        qry = "DELETE FROM notifications WHERE id = %d" % (n_id)
        self.mycursor.execute(qry)
        self.commit_all()
        return

    # new updata
    # add reading

    def update_notifications_by_nid(self, n_id):
        """update_notifications_by_nid(n_id): update notifications by notifications id
        @param n_id(int): notifications id to look up
        @return (None)"""
        qry = "UPDATE notifications SET is_read = TRUE WHERE id = %d" % (n_id)
        self.mycursor.execute(qry)
        self.commit_all()

    # new updata
    # add numbers of return all unread notifications

    def get_unread_notifications_by_uid(self, u_id):
        """ get_unread_notifications_by_uid(u_id): get unread notifications by user id
        @param u_id(int): user id to look up
        @return (tuple): a tuple of user's unread notifications"""
        data = sql_select_sorting(
            self.db, self.mycursor, "notifications", "u_id", u_id, "is_read", False, None, 1)
        # have how many tuple is how many unread
        return self.return_tuple(data)

    # add notifications for acts

    def add_notifications_host(self, notifications):
        """add a notification in data manager
        @param notifications(str): notifications content
        @return (int): new generated n_id"""
        notifications["message"] = self.db.escape_string(
            notifications["message"])
        qry = "INSERT INTO host_notifications (act_id, message, time) VALUES ( %d, '%s', '%s')" % (
            notifications["act_id"], notifications["message"], notifications["time"])
        self.mycursor.execute(qry)
        self.commit_all()
        return get_now_id("host_notifications", self.mycursor)

    def get_act_notification_by_aid(self, a_id):
        """ get all notifications by act id
        @param a_id(int): act id to look up
        @return (tuple): a tuple of act's notifications"""
        data = sql_select_sorting(
            self.db, self.mycursor, "host_notifications", "act_id", a_id, None, None, None, 1)
        return self.return_tuple(data)

    # booking host

    def is_sub_uid_hid(self, u_id, h_id):
        """is_sub_uid_hid(u_id, h_id): checks if user is the host of the act
        @param u_id(int): user id to look up
        @param h_id(int): host id to look up
        @return (bool): True if user is the host of the act, False otherwise"""
        qry = "SELECT * FROM subscribes WHERE user_id = %d AND host_id = %d" % (
            u_id, h_id)
        self.mycursor.execute(qry)
        data = self.mycursor.fetchall()

        return self.return_boolean(data)

    def add_host_sub(self, u_id, h_id):
        """add a user sub host in data manager
        @param u_id(int): user id to add
        @param h_id(int): host id to add
        @return (None)"""

        qry = "INSERT INTO subscribes (user_id, host_id) VALUES (%d, %d)" % (
            u_id, h_id)
        self.mycursor.execute(qry)
        self.commit_all()

    def get_user_sub_by_hid(self, h_id):
        """ get all user sub by host id
        @param h_id(int): host id to look up
        @return (tuple): a tuple of host's user sub"""
        data = sql_select_sorting(
            self.db, self.mycursor, "subscribes", "host_id", h_id, None, None, None, 1)
        return self.return_tuple(data)

    def delete_host_sub(self, u_id, h_id):
        """delete a user sub host in data manager
        @param u_id(int): user id to delete
        @param h_id(int): host id to delete
        @return (None)"""
        qry = "DELETE FROM subscribes WHERE user_id = %d AND host_id = %d" % (
            u_id, h_id)
        self.mycursor.execute(qry)
        self.commit_all()

    # donot care the act finish or not

    def get_most_popular_activities(self):
        """ get most popular activities
        @return (tuple): a tuple of most popular activities"""
        qry = "SELECT * FROM acts WHERE id in (SELECT act_id FROM booking_information GROUP BY act_id ORDER BY count(*) DESC)"
        self.mycursor.execute(qry)
        data = self.mycursor.fetchall()
        return data

    def get_rate_with_actid(self):
        """ get rate with act id
        @return (tuple): a tuple of rate with act id"""
        qry = "SELECT u_id, act_id, rating FROM commits WHERE reply_id = 0 AND h_id is NULL AND message != 'DELETE ALREADY' AND rating is not NULL ORDER BY u_id ASC"
        self.mycursor.execute(qry)
        data = self.mycursor.fetchall()
        return data

    # time

    def set_timenow(self, time):
        """set time now
        @param time(str): time to set
        @return (None)"""
        qry = "DELETE FROM timetables"
        self.mycursor.execute(qry)
        qry = "INSERT INTO timetables (now_time) VALUES ('%s')" % (time)
        self.mycursor.execute(qry)
        self.commit_all()

    def is_have_time(self):
        """is_have_time(): checks if have time
        @return (bool): True if have time, False otherwise"""
        qry = "SELECT now_time FROM timetables ORDER BY id DESC LIMIT 1"
        self.mycursor.execute(qry)
        data = self.mycursor.fetchall()
        return self.return_boolean(data)

    def get_timenow(self):
        """ get database time now
        @return (str): time now"""
        qry = "SELECT now_time FROM timetables ORDER BY id DESC LIMIT 1"
        self.mycursor.execute(qry)
        data = self.mycursor.fetchall()
        return self.return_record(data)[0]

    def push_time(self, time):
        """push time to database
        @param time(str): time to push
        @return (None)"""
        qry = "UPDATE timetables SET now_time = '%s' ORDER BY id DESC LIMIT 1" % (
            time)
        self.mycursor.execute(qry)
        self.commit_all()

    # email check

    def add_email_validation(self, email, validation):
        """add a email validation in data manager
        @param email(str): email to add
        @param validation(str): validation to add
        @return (None)"""
        qry = "DELETE FROM email_validation WHERE email = '%s'" % (email)
        self.mycursor.execute(qry)
        self.commit_all()
        qry = "INSERT INTO email_validation (email, validation) VALUES ('%s', '%s')" % (
            email, validation)
        self.mycursor.execute(qry)
        self.commit_all()

    def get_email_validation_by_email(self, email):
        """ get email validation by email
        @param email(str): email to look up
        @return (tuple): a tuple of email validation"""
        qry = "SELECT * FROM email_validation WHERE email = '%s'" % (email)
        self.mycursor.execute(qry)
        data = self.mycursor.fetchall()
        return self.return_record(data)

    def delete_email_validation_by_uid(self, email):
        """delete a email validation in data manager
        @param email(str): email to delete
        @return (None)"""
        qry = "DELETE FROM email_validation WHERE email = '%s'" % (email)
        self.mycursor.execute(qry)
        return self.commit_all()

    def get_all_info(self):
        """ get all info
        @return (tuple): a tuple of all info"""
        user_num = get_now_id('customers', self.mycursor)
        host_num = get_now_id('hosts', self.mycursor)
        act_num = get_now_id('acts', self.mycursor)
        commit_num = get_now_id('commits', self.mycursor)
        order_num = get_now_id('booking_information', self.mycursor)
        return user_num, host_num, act_num, commit_num, order_num

    def get_sell_act(self):
        """ get sell act
        @return (tuple): a tuple of sell act"""
        qry = "SELECT id, name, description, all_ticket, possible_seats, ticket_money FROM acts Order by (all_ticket - possible_seats)*ticket_money DESC"
        self.mycursor.execute(qry)
        data = self.mycursor.fetchall()
        return data

    # OTHER

    def clear_data(self):
        """clear(): clear all data and reset to initial status
        @param (None)
        @return (None):"""
        qry = "DROP DATABASE IF EXISTS mymyunsw;"
        self.mycursor.execute(qry)
        self.commit_all()

    def clear_token(self):
        qry = "Update customers SET tokens = NULL"
        self.mycursor.execute(qry)
        qry = "Update hosts SET tokens = NULL"
        self.mycursor.execute(qry)
        self.commit_all()

    def close(self):
        """close(): close the connection
        @param (None)
        @return (None):"""
        # self.mycursor.close()
        self.db.close()

    # helper
    # using for return values

    def return_boolean(self, data):
        return data != ()

    def return_record(self, data):
        return data[0] if data != () else None

    def return_int(self, data):
        return data[0][0] if data != () else None

    def return_tuple(self, data):
        return data if data != () else None

    def commit_all(self):
        self.db.commit()


dm = DataManager()
