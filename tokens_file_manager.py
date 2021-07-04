
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

def printTokensToExcel(usersIds_tokens,usersIds_imagesGuid):
    # Workbook is created
    wb = Workbook()
    # add_sheet is used to create sheet.
    index=1
    sheet = wb.add_sheet(str(index))
    sheet.col(0).width  = 256 * 35 # 40 characters wide (-ish)
    sheet.col(1).width  = 256 * 200 # 300 characters wide (-ish)
        
    
    index=addSumDetailsToExcel(sheet,index)
    labels = ['User ID','Token']
    index=addLabelsToExcelSheet(labels,sheet,index)
    index=addTokensToExcelSheet(sheet,index,usersIds_tokens,usersIds_imagesGuid)
    
        
    wb.save('tokens-Without-Images-File.xls') 
    
def addSumDetailsToExcel(sheet,index):    
    sheet.write(index, 0, 'Date : ',grayBold)
    sheet.write(index, 1, str(date.today()),gray)
    return index +1  

def addLabelsToExcelSheet(labels,sheet,index):
    index+=2  
    for col in range(0,len(labels)):
        sheet.write(index, col, labels[col],gray25Bold)
    return index+1
        
def addTokensToExcelSheet(sheet,index,usersIds_tokens,usersIds_imagesGuid):
    for userId in usersIds_imagesGuid: 
        if len(usersIds_imagesGuid[userId])==0:
            sheet.write(index, 0,userId ,whiteStyle)
            if userId in usersIds_tokens:
                sheet.write(index, 1,usersIds_tokens[userId] ,whiteStyle)
            else: 
                sheet.write(index, 1,'Not existing',whiteStyle)
            index+=1
    return index+1
  
       
       

            
        