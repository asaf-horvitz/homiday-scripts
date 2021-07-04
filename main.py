
from firebase_init import *
from msgs_manager import *
from msgs_file_manager import * 
from tokens_file_manager import * 
import time

start = time.time()



MAIN_PATH ='production' # debug or production
LAST_DAYS = 300
GEN_MSGS =True
GEN_TOKENS =False
# connect_to_db()
db = get_db()
all_msgs=[]
last_msgs = []
chats ={}
usersIds = {}
users_locality = {}
usersIds_tokens = {}
usersIds_imagesGuid = {}


main_ref = db.collection(MAIN_PATH).document(MAIN_PATH)
msgs_ref = main_ref.collection('msgs').document('msgs')
chat_msgs_ref= msgs_ref.collection('chat-msgs')
pub_profile_ref = main_ref.collection('public-profiles')
private_profiles_ref = main_ref.collection('private-profiles')





if GEN_MSGS:
    docs = chat_msgs_ref.stream()
    for doc in docs:
        all_msgs.append(doc.to_dict())
        
    msgManager = MsgsManager()

    print (f'len of all msgs : {len(all_msgs)}')

    msgManager.msgs_statistics(all_msgs)    

    last_msgs=msgManager.filterMsgsFromLastDays(LAST_DAYS,all_msgs)

    print (f'len after filter all msgs : {len(last_msgs)}')

    chats = msgManager.getAllchats(last_msgs)
    chats = msgManager.prepareChatsTofile(chats)

    docs = pub_profile_ref.stream()
    for doc in docs:
        dict = doc.to_dict()
        userId=dict['userId']
        usersIds[userId]=  dict['houseName']
        if 'locality' in dict['location']['geoLocation']['regions']:      
            users_locality[userId]=dict['location']['geoLocation']['regions']['locality']
        else :
            users_locality[userId]='None'
    printChatsToExcel(usersIds,chats,users_locality)
    print('------------------Sum MSGS-------------------')
    print(f'Num of userIds : {len(usersIds)}')
    print(f'Num of chats : {len(chats)}') 
    print(f'Num of Phones number : {msgManager.getNumOfPhoneNum()}') 

if GEN_TOKENS:  
    docs = private_profiles_ref.stream()
    for doc in docs:
        userId=doc.to_dict()['userId']
        if 'notificationToken' in doc.to_dict():
            usersIds_tokens[userId] = doc.to_dict()['notificationToken']
        usersIds_imagesGuid[userId] = doc.to_dict()['imagesGuid']    
    printTokensToExcel(usersIds_tokens,usersIds_imagesGuid)
    print('------------------Sum Tokens-------------------')
    print(f'Num of userIds : {len(usersIds_tokens)}')


end = time.time()
print(f'measured Time: {end - start}')









