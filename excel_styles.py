import xlwt

def getCellStyle(color,bold=False):
    style = xlwt.XFStyle()
    # warp text 
    style.alignment.wrap = 1
    # font
    font = xlwt.Font()
    font.bold = bold
    style.font = font
    #color 
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map[color]
    style.pattern = pattern
    return style


grayBold = getCellStyle('gray40',True)
gray = getCellStyle('gray40')
gray25Bold = getCellStyle('gray25',bold=True)
whiteStyle = getCellStyle('white')
yellow = getCellStyle('yellow')
