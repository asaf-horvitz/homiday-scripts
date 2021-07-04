from datetime import date
# from datetime import datetime
import datetime




class MsgsManager:
    phone_num = 0 

    total_msgs_per_day = {}
    total_phone_exchanged_per_day = {}

    def __init__(self):
        self.init_statistics()
        pass
    
    def init_statistics(self):
        start_date = datetime.date(2021, 4, 1)
        end_date = datetime.date.today()
        delta = datetime.timedelta(days=1)
        while start_date <= end_date:
            self.total_msgs_per_day[start_date] = 0
            self.total_phone_exchanged_per_day[start_date] = 0
            start_date += delta

    def get_details_of_msg(self, msg):
        return msg['to'], msg['from'], msg['msgTime'].date(), msg['msg']

    def get_conversation_key(self, to_user, from_user):
        if to_user > from_user:
            return from_user + '-' + to_user
        return to_user + '-' + from_user
    
    def msgs_statistics(self, msgs):
        for msg in msgs:
            to_user, from_user, msg_date, content = self.get_details_of_msg(msg)
            if (msg_date in self.total_msgs_per_day):
                self.total_msgs_per_day[msg_date] += 1
            if self.phone_number_in_msg(content) and (msg_date in self.total_phone_exchanged_per_day):
                self.total_phone_exchanged_per_day[msg_date] += 1
        self.write_statistics()

    def write_statistics(self):
        total_msgs_per_day_file = open("c:/tmp/total_msgs_per_day.csv", "w")
        total_phone_exchanged_per_day_file = open("c:/tmp/total_phone_exchanged_per_day.csv", "w")
        for curr_date in self.total_msgs_per_day:
            curr_date_str = curr_date.strftime("%m/%d/%Y")
            total_msgs_per_day_file.write(curr_date_str + ',' + str(self.total_msgs_per_day[curr_date]) + '\n')
            total_phone_exchanged_per_day_file.write(curr_date_str + ',' + str(self.total_phone_exchanged_per_day[curr_date])+ '\n')
        total_msgs_per_day_file.close()


    def phone_number_in_msg(self, content):
        return content.find('05') !=-1 or content.find('972') !=-1 

    
    def filterMsgsFromLastDays(self,num_of_days,msgs):
        new_msgs =[]
        for msg in msgs:
            utc_time = msg['msgTime']
            last_days = date.today() + datetime.timedelta(days=-num_of_days)

            if (last_days <= utc_time.date()):
                new_msgs.append(msg)
        return new_msgs
    
    def checkNone(self,v):
        if v==None :
            return 'None'
        else: return v
        
    def getChatId(self,id1,id2):
        id1=self.checkNone(id1)
        id2=self.checkNone(id2)
        if id1>id2:
            return f'{id1}#{id2}'
        else:
            return f'{id2}#{id1}'

    def getAllchats(self,msgs):
        chats = {}
        for msg in msgs:
            chat_id = self.getChatId(msg['from'],msg['to']) 
            if chat_id in chats:
                chats[chat_id].append(msg)
            else: 
                chats[chat_id] = [msg]
        
        return chats
    
        
    
        
    def prepareChatsTofile(self,chats):
        
        for chat_id in chats:
            isPhone =False
            for msg in chats[chat_id]:
                msg.pop('to')
                if self.isPhoneNumber(msg):
                    isPhone=True
            
            chats[chat_id].sort(key=self.compereMsgsByDate)
            if isPhone: self.phone_num+=1
        
        #############chats = {id1#id2 : [msg1,msg2...msg3]}
        #############msg = {....., 'msgTime' :date()}
        chats = dict(sorted(chats.items(), key=lambda item: self.compereChatsByLastDate(item[1]),reverse=True))
        # chats = dict(sorted(chats.items(), key=lambda item: compereChatsByPhoneNumber(item[1]),reverse=True))
        return chats
        
    def getNumOfPhoneNum(self):
        return self.phone_num
                
                
                
    def compereMsgsByDate(self,msg):
        return msg['msgTime']

    def compereChatsByLastDate(self,msgs):
        return msgs[-1]['msgTime']

    def compereChatsByPhoneNumber(self,msgs):
        for msg in msgs: 
            if self.isPhoneNumber(msg):
                return 1
        return 0

    def isPhoneNumber(self,msg):
        return msg['msg'].find('05') !=-1 or msg['msg'].find('972') !=-1 

  
        


