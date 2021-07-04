from datetime import date
import xlwt
from xlwt import Workbook
from excel_styles import *

# def getCellStyle(color,bold=False):
#     style = xlwt.XFStyle()
#     # warp text 
#     style.alignment.wrap = 1
#     # font
#     font = xlwt.Font()
#     font.bold = bold
#     style.font = font
#     #color 
#     pattern = xlwt.Pattern()
#     pattern.pattern = xlwt.Pattern.SOLID_PATTERN
#     pattern.pattern_fore_colour = xlwt.Style.colour_map[color]
#     style.pattern = pattern
#     return style


# grayBold = getCellStyle('gray40',True)
# gray = getCellStyle('gray40')
# gray25Bold = getCellStyle('gray25',bold=True)
# whiteStyle = getCellStyle('white')
# yellow = getCellStyle('yellow')


def printChatsToExcel(usersIds,chats,users_locality):
    # Workbook is created
    wb = Workbook()
    # add_sheet is used to create sheet.
    index=1
    sheet = wb.add_sheet(str(index))
    sheet.col(0).width  = 256 * 35 # 40 characters wide (-ish)
    sheet.col(1).width  = 256 * 60 # 40 characters wide (-ish)
    sheet.col(2).width  = 256 * 60 # 40 characters wide (-ish)
    sheet.col(3).width  = 256 * 35 # 40 characters wide (-ish)
    
    
    index=addSumDetailsToExcel(sheet,index,usersIds,chats)
    for chatId in chats:
        houseName1= getHouseName(chatId.split("#")[0],usersIds)   
        houseName2= getHouseName(chatId.split("#")[1],usersIds)
        labels = ['Date',houseName1,houseName2]
        index=addChatDetailesToExcelSheet(chatId,usersIds,sheet,index,users_locality)
        index=addChatLabelsToExcelSheet(labels,sheet,index)
        index=addMsgsToExcelSheet(chats[chatId],chatId.split("#")[0],sheet,index)
         
    wb.save('chatsLastDays.xls') 
    
def addSumDetailsToExcel(sheet,index,usersIds,chats): #TODO add detailes for usersIds and chats 
    sheet.write(index, 0, 'Date : ',grayBold)
    sheet.write(index, 1, str(date.today()),gray)
    index+=1 
    return index +1  

def addChatLabelsToExcelSheet(labels,sheet,index):
    index+=2
    for col in range(0,len(labels)):
        sheet.write(index, col, labels[col],gray25Bold)
    return index+1
        
def addMsgsToExcelSheet(msgs,id1,sheet,index):
    # for row in range(index,len(msgs)+index):
    for msg in msgs: 
        # msg=msgs[row-index]
        sheet.write(index, 0, str(msg['msgTime']))
        if msg['from']==id1:
            sheet.write(index, 1, msg['msg'],whiteStyle)
        else:
            sheet.write(index, 2, msg['msg'],whiteStyle)
        index+=1
    sheet.write(index, 0, '',yellow)
    sheet.write(index, 1, '',yellow)
    sheet.write(index, 2, '',yellow)
    return index+1
  
def addChatDetailesToExcelSheet(chatId,usersIds,sheet,index,users_locality): 
    for ix in range(0,2):
        index+=1
        sheet.write(index, 0, f'houseName{ix+1} \n Locality :  ',grayBold)
        if chatId.split("#")[ix] in users_locality:
            locality = users_locality[chatId.split("#")[ix]]
        else: locality = 'Removed User'
        sheet.write(index, 1, f'{getHouseName(chatId.split("#")[ix],usersIds)}\n{locality}'  ,gray)
        sheet.write(index, 2, f'Id{ix+1} : ',grayBold)
        sheet.write(index, 3, chatId.split("#")[ix],gray)
    
    return index+1
        
        #3
def getHouseName(id,usersIds):
    if id in usersIds:
        return usersIds[id]
    else : 
        return 'Remove house'
    
    
    

         
            
        