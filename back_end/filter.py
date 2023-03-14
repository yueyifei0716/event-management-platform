# DFA algorithm from website


class DFAUtils(object):

    def __init__(self, word_warehouse):
        
        self.root = dict()
        self.skip = [' ', '&', '!', '@', '#', '$', '*', '^', '%', '?', '<', '>']
        for word in word_warehouse:
            self.add_word(word)

    def add_word(self, word):
        
        now_word = self.root
        word_count = len(word)
        for i in range(word_count):
            char_str = word[i]
            if char_str in now_word.keys():
                
                now_word = now_word.get(word[i])
                now_word['is_end'] = False
            else:
                
                new_word = dict()

                if i == word_count - 1:  
                    new_word['is_end'] = True
                else:  
                    new_word['is_end'] = False

                now_word[char_str] = new_word
                now_word = new_word

    def check_match_word(self, message, index, match_type = 1):
        
        flag = False
        match_flag_length = 0  
        now_map = self.root
        temp = 0  

        for i in range(index, len(message)):
            word = message[i]

            if word in self.skip and len(now_map) < 100:
                temp += 1
                continue

            now_map = now_map.get(word)
            if now_map: 
                match_flag_length += 1
                temp += 1
                if now_map.get("is_end"):
                    flag = True
                    if match_type == 1:
                        break
            else:  
                break

        if temp < 2 or not flag:  
            temp = 0
        return temp

    def get_match_word(self, message, match_type = 1):
        
        matched_word_list = list()
        for i in range(len(message)):  # 0---11
            length = self.check_match_word(message, i, match_type)
            if length > 0:
                word = message[i:i + length]
                word = word.replace(" ", "")
                matched_word_list.append(word)
                # i = i + length - 1
        return matched_word_list

    def is_contain(self, message, match_type = 1):
        
        flag = False
        for i in range(len(message)):
            match_flag = self.check_match_word(message, i, match_type)
            if match_flag > 0:
                flag = True
        return flag

    def replace_match_word(self, message, replace_char='*', match_type = 1):
        
        result_message = ""

        tuple_set = self.get_match_word(message, match_type)
        word_set = [i for i in tuple_set]
        
        if len(word_set) > 0:  
            for word in word_set:
                replace_string = len(word) * replace_char
                message = message.replace(word, replace_string)
                result_message = message
        else:  
            result_message = message
        return result_message

