import threading
import pymysql



def begin_db (mycursor):
    
    """
    Description:
        Stores and manages user/channel/message data according to the
        following rules. All [user]s, [channel]s and [message]s should be
        formatted exactly as is shown below.
        
        host = {
            'email': 'cs1531@cse.unsw.edu.au',
            'password': 'justapassword',
            'hold_active': [1,2],  # act_id (act id)
            'tokens': ["441fc1cb0032cf076889b3c274faf3d4ab9f789443b4c6a00f5b3eb19793df28"]
        }
        # 取消的时候，检查这个act是不是在这个列表里
        user = {
            'email': 'cs1531@cse.unsw.edu.au',
            'name_first': 'Hayden',
            'name_last': 'Jacobs',
            'address': 'haydenjacobs',
            'password': 'justapassword',
            'bill_method': 'visa',
            'join_in_act': [1,2],  # act_id (act id)
            'tokens': ["441fc1cb0032cf076889b3c274faf3d4ab9f789443b4c6a00f5b3eb19793df28"]
        }
        act = {
            'name': 'My Act',
            'description': 'This is my act',
            'type': 'music',
            'venue_name': 'Theatre',
            'venue_address': 'UNSW',
            'start_time': 12:30,
            'end_time': 12:31,
            'start_date': 2020/02/02,
            'end_date': 2020/02/04,
            'all_ticket': 100,
            'possible_seats: 100,
            'ticket_money': 309
            'standup': [booking_information],
            'commit': [commit]
        }
        # 这里要写一个可行的检查座位是否空闲
        
        booking_information = {
            'u_id': 1, # u_id (user id)
            'seat': 8/12, # seat (seat number)
        }
        
        commit = {
            'u_id': 1, # u_id (user id)
            'commit': ' I donot like it'
        }
        self.[data]s = {id1: [data]1, ...}
    Note:
        Please make sure your parameters are valid.
        This module only deals with storage.
        Please give the complete data(a dict) of user/channel/message params as above.
    """ 
    
    # Create tables
    # create table user
    qry = """
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL, 
            password VARCHAR(255) NOT NULL, 
            name_first VARCHAR(255),
            name_last VARCHAR(255), 
            address VARCHAR(255), 
            bill_method enum('bpay', 'visa', 'wechat') NOT NULL,
            account VARCHAR(255) NOT NULL, 
            tokens VARCHAR(255), 
            balance Float
        )
        
    """
    # bill_method enum('bpay', 'visa', 'wechat') NOT NULL,
    mycursor.execute(qry)
    
    # create table host
    qry = """
        CREATE TABLE IF NOT EXISTS hosts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL, 
            password VARCHAR(255) NOT NULL,  
            tokens VARCHAR(255)
        )
        
    
    """
    # type ENUM('music', 'magical')
    mycursor.execute(qry)

    # create table acts
    qry = """
        CREATE TABLE IF NOT EXISTS acts (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            hold_host INT NOT NULL, 
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            type ENUM('music', 'magical'),
            venue_name VARCHAR(255),
            venue_address VARCHAR(255), 
            start_time TIME,
            end_time TIME,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            all_ticket INT NOT NULL,
            possible_seats INT,
            ticket_money Float,
            seat_x INT,
            seat_y INT,
            image LongText,
            FOREIGN KEY (hold_host) references hosts(id)
        )
        
    """
    mycursor.execute(qry)
    
    # mycursor.execute("alter table acts add constraint hold_host foreign key(hold_host) references hosts(id)")

    # join_in_act -> acts table
    # create table booking_information  
    # saving information of user booking acts
    qry = """
        CREATE TABLE IF NOT EXISTS booking_information (
            id INT AUTO_INCREMENT PRIMARY KEY,
            x INT, 
            y INT, 
            u_id INT NOT NULL, 
            act_id INT NOT NULL, 
            FOREIGN KEY (u_id) references customers(id), 
            FOREIGN KEY (act_id) references acts(id)
        )
        
    """
    mycursor.execute(qry)
            
    # coustomer_id -> customers table
    # create table commits
    qry = """
        CREATE TABLE IF NOT EXISTS commits (
            id INT AUTO_INCREMENT PRIMARY KEY,
            h_id INT, u_id INT, 
            act_id INT NOT NULL, 
            message VARCHAR(255), 
            reply_id INT, 
            time datetime not null,
            rating enum ('0','1','2','3','4','5','6','7','8','9','10', 'None'),
            FOREIGN KEY (h_id) references hosts(id), 
            FOREIGN KEY (u_id) references customers(id), 
            FOREIGN KEY (act_id) references acts(id)
        )
        

    """
    # rating enum ('0','1','2','3','4','5','6','7','8','9','10', 'None'),
    mycursor.execute(qry)
    
    # create table notifications
    qry = """
        CREATE TABLE IF NOT EXISTS notifications (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            u_id INT, 
            message VARCHAR(255), 
            act_id INT, 
            is_read BOOLEAN, 
            time datetime,
            FOREIGN KEY (u_id) references customers(id), 
            FOREIGN KEY (act_id) references acts(id)
            
        )
        
    
    """
    
    mycursor.execute(qry)
    
    # private table   timetable
    qry = """
        CREATE TABLE IF NOT EXISTS timetables (
            id INT AUTO_INCREMENT PRIMARY KEY,
            now_time datetime not null
        )
    
    """
    mycursor.execute(qry)
    
    # create table host_book -> subscribe
    qry = """
        CREATE TABLE IF NOT EXISTS subscribes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            host_id INT NOT NULL,
            user_id INT NOT NULL,
            FOREIGN KEY (host_id) references hosts(id),
            FOREIGN KEY (user_id) references customers(id)
        )
    """
    mycursor.execute(qry)
    
    # create table notification of acts
    qry = """
        CREATE TABLE IF NOT EXISTS host_notifications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            act_id INT NOT NULL,
            message VARCHAR(255) NOT NULL,
            time datetime not null
        )
    """
    mycursor.execute(qry)
    
    # create table email verification
    qry = """
        CREATE TABLE IF NOT EXISTS email_validation (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            validation VARCHAR(255) NOT NULL
        )
    """
    mycursor.execute(qry)   
    
    return mycursor


# Simplify query statements and improve reuse
def sql_select_sorting(db, mycursor, table, head1, value1, head2, value2, sort, kind):
    threadLock = threading.Lock()
    threadLock.acquire()
    qry_sort = check_sort(sort, kind, db)
    # Preventing sql injection
    # Concatenate multiple query statements
    table = db.escape_string(table)
    qry = "SELECT * FROM " + table + ' '
    qry_frist = frist_check(head1, value1, db)
    qry_second = second_check(head2, value2, db)
    qry = qry + qry_frist + qry_second + qry_sort

    mycursor.execute(qry)
    data = mycursor.fetchall()
    threadLock.release()
    return data

# Check whether the query has sorting requirements
def check_sort(sort, kind, db):
    if sort == None:
        return ""
    sort = db.escape_string(sort)
    qry = "Order by " + sort +  " ASC"
    if int(kind) < 0:
        qry = "Order by " + sort +  " DESC"
    return qry

# Check the first query requirement
def frist_check(head, value, db):
    if value == None:
        return ""
    head = db.escape_string(head)
    if (not isinstance(value, int)) and (not isinstance(value, float)):
        value = db.escape_string(value)
    qry = " WHERE %s = '%s'" % (head, value)
    return qry       


#Check the second query requirement
def second_check(head, value, db):

    if value == None:
        return ""
    head = db.escape_string(head)
    if (not isinstance(value, int)) and (not isinstance(value, float)):
        value = db.escape_string(value)
    qry = " AND %s = '%s'" % (head, value)
    return qry       


# Fuzzy matching query is used and sql is used to prevent injection.
def sql_match(db, mycursor, table, head, value):
    table = db.escape_string(table)
    head = db.escape_string(head)
    if (not isinstance(value, int)) and (not isinstance(value, float)):
        value = db.escape_string(value)
    qry = "SELECT * FROM " + table + ' WHERE ' + head + ' like \'%' + value + '%\' Order by ' + head + ' ASC'
    mycursor.execute(qry)
    data = mycursor.fetchall()
    return data


# Helper function to get the latest id
def get_now_id(table, mycursor):
    qry = "SELECT max(id) from %s" % (table)
    mycursor.execute(qry)
    data = mycursor.fetchone()
    return data[0]
    
def get_userbyid(id, mycursor):
    qry = "SELECT * FROM customers WHERE id = %s" % (id)
    mycursor.execute(qry)
    data = mycursor.fetchall()
    return data

def get_userbytoken(token, mycursor):
    qry = "SELECT * FROM customers WHERE tokens ='%s'"% (token)
    mycursor.execute(qry)
    data = mycursor.fetchall()
    return data


# def sql_most_often():
#     qry1 = """
#     create or replace view get_id(id)
#     as
#         select beer
#         from brewed_by
#         group by beer 
#         having count(brewery) > 1
#     ;
#     """