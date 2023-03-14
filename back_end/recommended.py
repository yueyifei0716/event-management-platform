from math import sqrt
from data_sql import dm


class RecommendationSystem:
    
    def __init__(self, uid):
        self.search_uid = uid
        self.data_record = dm.get_rate_with_actid()
        # self.data_record = d
        
    
    def get_data(self):
        # get the data from the database
        data = self.data_record
        data_u = {}
        for i in data:
            u_id, act_id, rating = i
            data_u.setdefault(u_id,{})
            data_u[u_id][act_id] = (rating) 
        return data_u
        

    def calculate(self):
        list_data = self.get_data()
        user_diff = {}

        if not self.search_uid in list_data.keys():
            return None
        for act in list_data[self.search_uid]:
            user_diff = self.make_matix(user_diff, act, list_data)

        # Filter userself when calculating the similarity of other users.
        DELETE_list = []
        DELETE_list.append(self.search_uid)
        for i in user_diff.keys():
            if user_diff[i] == {}:
                DELETE_list.append(i)
        for i in DELETE_list:
            del user_diff[i]
        return user_diff


    def make_matix(self, user_diff, act, list_data):
        # using matrix to calculate the similarity
        for people in list_data.keys():
            user_diff.setdefault(people,{})
            for item in list_data[people].keys():
                self.two_deep_helper(item, act, people, user_diff, list_data)
        return user_diff

                    
    def two_deep_helper(self, item, act, people, user_diff, list_data):
        if item == act:
            # git rid of the same act
            diff = pow(int(list_data[self.search_uid][act]) - int( list_data[people][item]),2)
            user_diff[people][item] = diff
                    

    def people_rating(self):
        # get the people who have the same act with the user
        user_diff = self.calculate()
        if user_diff == None:
            return None
        rating = {}
        for people in user_diff.keys():
            rating.setdefault(people,{})
            a = 0
            b = 0
            for score in user_diff[people].values():
                a += score
                b += 1
            a = sqrt(a)
            rating[people] = float(1/(1+(a/b)))
        return rating


    def top_list(self):
        # get the top 5 activity
        list_data = self.people_rating()
        if list_data == None:
            return None
        items = list_data.items()
        top = [[v[1],v[0]] for v in items]
        top.sort(reverse=True)
        return top[0:5]
        
    def find_rec(self):
        rec_list = self.top_list()
        if rec_list == None:
            return []

        all_list = self.get_data()
        list_act = []
        # find every record and put it into the list
        for i in range(0,len(rec_list)):
            j = rec_list[i][1]
            for k,v in all_list[j].items():
                if k not in all_list[self.search_uid].keys() and v not in list_act:
                    list_act.append(k)

        return list_act
 



   
  