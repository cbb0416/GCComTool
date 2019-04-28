from PIL import Image, ImageDraw, ImageFont
import xlrd
import re

def draw_image(new_img, text, font_size=40,show_image=False):
    text = str(text)
    draw = ImageDraw.Draw(new_img)
    img_size = new_img.size
    #draw.line((0, 0) + img_size, fill=128)
    #draw.line((0, img_size[1], img_size[0], 0), fill=128)
 
    #fnt = ImageFont.truetype('simhei.ttf', font_size)
    #fnt = ImageFont.truetype('simsun.ttc', font_size)  #宋体
    fnt = ImageFont.truetype('SOURCEHANSANSCN-REGULAR.OTF', font_size)  #思源
    
    
    fnt_size = fnt.getsize(text)
    fnt_color = (253,54,54)#红色
    #fnt_color = (77,224,77)#绿色
    #print(fnt_size)
    #print(img_size)
    if (fnt_size[1] > img_size[1]):#文字高度大于图片高度
        #print('Waring!!!!!!!!!!!!!Font size is lager than Image size')
        return

    if (font_size == 0):
        return
    
    line_num = (int)((fnt_size[0]-1)/img_size[0])+ 1 #计算占用行数
    if (line_num == 1):
        draw.text((0,(img_size[1]- font_size)/2), text, font=fnt, fill=fnt_color)
        #print('one line')
    else:
        #print('multi line, text_len:' + str(len(text)))
        current_text_cnt = 0        #已处理的文本数量计数
        current_line = 0            #当前处理行
        draw_text = ''              #待绘制的文本
        pre_draw_text = ''
        draw_line_pixal_cnt = 0     #待绘制行占用像素计数
        
        
        for ch in text:
            #ch_size = fnt.getsize(ch)
            #if ch_size[0] <= fnt_size[1]/2:
            #    draw_line_pixal_cnt += fnt_size[1]/2   #ASCII字符，占用字体宽度一半
            #else:
            #    draw_line_pixal_cnt += fnt_size[1]     #中文字符
            pre_draw_text += ch
            text_pixal = fnt.getsize(pre_draw_text)
            draw_line_pixal_cnt = text_pixal[0]
            current_text_cnt += 1

            #print('draw_line_pixal_cnt:' + str(draw_line_pixal_cnt) + '  current_text_cnt:' + str(current_text_cnt))
            
            if draw_line_pixal_cnt >= img_size[0]:   #待显示行内容占用像素超出图片宽度
                if draw_line_pixal_cnt == img_size[0]:
                    draw_text += ch
                line_str = ''
                line_text_cnt = 0
                draw.text((0, current_line*fnt_size[1]), draw_text, font=fnt, fill=fnt_color)
                draw_line_pixal_cnt = 0
                draw_text = ''#清空待显示的文本
                pre_draw_text = ''
                #print('draw 1')
                current_line += 1 #标记对下一行进行处理
                if current_line >= 2:   #最多显示两行
                    #print('break')
                    break
                else:
                    #print('continue')
                    if current_text_cnt >= len(text):
                        #print('str_len_cnt >= len(text)')
                        draw_text = ch
                        draw.text((0,current_line*fnt_size[1]), draw_text, font=fnt, fill=fnt_color)
                        #print('draw 2')
                        break
                    else:
                        draw_text += ch
                        pre_draw_text += ch
                        text_pixal = fnt.getsize(pre_draw_text)
                        draw_line_pixal_cnt = text_pixal[0]
                        continue
            else:
                draw_text += ch
            
            if current_text_cnt >= len(text):
                #print('str_len_cnt >= len(text)')
                draw.text((0,current_line*fnt_size[1]), draw_text, font=fnt, fill=fnt_color)
                #print('draw 2')
                

    if show_image:
        new_img.show()
    del draw
 
 
def new_image(image_name, width, height, text='default', color=(255, 255, 255, 0),show_image=False):
    new_img = Image.new('RGBA', (int(width), int(height)), color)
    draw_image(new_img, text, 25, show_image)
    #new_img.save(r'%s_%s_%s.png' % (width, height, text))
    new_img.save(r'%s.png' % image_name)
    del new_img
 
 
def new_image_with_file(fn):
    with open(fn, encoding='utf-8') as f:
        for l in f:
            l = l.strip()
            if l:
                ls = l.split(',')
                if '#' == l[0] or len(ls) < 2:
                    continue
 
                new_image(*ls)


# 中文标点符号转换成英文标点符号
def text_format_translate(text):
    table = {ord(f):ord(t) for f,t in zip(
     u'，。！？【】（）％＃＠＆１２３４５６７８９０',
     u',.!?[]()%#@&1234567890')}
    res = text.translate(table)
    return res

#去掉文件命名时的非法字符，并替换成下划线
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

def read_excel():
        ExcelFile=xlrd.open_workbook(r'华仪农机故障码列表.xlsx')
        SheetNames = ExcelFile.sheet_names()

        #打印sheet名称
        print('Sheet Names:')
        for name in SheetNames:
            print(name)
        print('')

        #创建故障代码映射表
        #fault_code_map_table = open("data.c",'w+')
        with open("engine_fault_code_table.c", "w+", encoding='gb2312') as f:
            #sheet表数量
            sheet_num = len(SheetNames)
            f.write(r'#include "engine_fault_code_table.h"')
            f.write('\r\r')
            
            #f.write('const uint16_t EngineStartIndex[' + str(sheet_num) +  '] = \r')
            f.write('const uint16_t EngineStartIndex[] = \r')
            f.write('{\r')
            f.write('    ')

            row = 0
            total_row = 0
            for sheet_names in SheetNames:
                sheet = ExcelFile.sheet_by_name(sheet_names)
                f.write(str(row+2) + ',')
                row += sheet.nrows - 1
                total_row += sheet.nrows - 1
            f.write('\r};\r\r')
            f.write('uint8_t EngineManufacturerNum = ' +  str(sheet_num) + ';\r')
            f.write('uint16_t EngineFaultCodeNum = ' +  str(total_row + 2) + ';\r\r')
            #f.write('const EngineFaultCodeMappingTable_t EngineFaultCodeMappingTable[' + str(total_row + 1) + '] = \r{\r')
            f.write('const EngineFaultCodeMappingTable_t EngineFaultCodeMappingTable[] = \r{\r')
            #f.write(r'//	FMI, SPN, Blink Code, Engine Fault Code Index')
            f.write(r'//	FMI, SPN')
            f.write('\r') 
            f.write(r'    {' + '0,0' +  '},//工作正常')
            f.write('\r') 
            f.write(r'    {' + '0,1' +  '},//CAN通信异常')
            
            Count = 0
            for sheet_names in SheetNames:
                sheet = ExcelFile.sheet_by_name(sheet_names)
                
                print('')
                print('***********************************************************')
                print('Sheet表名称: ',sheet.name,'，行数量:', sheet.nrows, '，列数量:', sheet.ncols)
                print('')

                f.write('\r' + r'//  ' + sheet.name + '\r')
                #生成绿色“工作正常”图片
                
                for rows in range(sheet.nrows):
                        if (rows == 0): #忽略第一行表头内容
                            file_name = validateTitle('工作正常')
                            disp_text = '                工作正常'
                            new_image(file_name, 296, 50, disp_text,color=(0, 0, 0, 0), show_image=False)

                            file_name = validateTitle('CAN通信异常')
                            disp_text = '             CAN通信异常'
                            new_image(file_name, 296, 50, disp_text,color=(0, 255, 0, 0), show_image=False)
                            continue
                        
                        Count += 1
                        #f.write(r'    {' + str(int(sheet.cell(rows,2).value)) + ',' + str(int(sheet.cell(rows,1).value)) + ',' + str(int(sheet.cell(rows,3).value)) + ',' + str(Count) + '},')
                        f.write(r'    {' + str(int(sheet.cell(rows,2).value)) + ',' + str(int(sheet.cell(rows,1).value)) +  '},')
                        f.write(r'//  ' + str(Count) + ',' + str(int(sheet.cell(rows,3).value)) + '-' + sheet.cell(rows,0).value + '\r')
                        
                        #print('Index:',Count,',故障内容:',sheet.cell(rows,0).value,',SPN:',int(sheet.cell(rows,1).value),',FMI:',int(sheet.cell(rows,2).value),',Blink Code:',int(sheet.cell(rows,3).value))
                        #if (rows == 10):
                        #        break
                        #file_name = validateTitle('#华仪发动机故障码' + '_' + str(Count) + '#' + str(int(sheet.cell(rows,3).value))+'_'+ text_format_translate(sheet.cell(rows,0).value))
                        file_name = validateTitle('#华仪发动机故障码' + '_' + str(Count) + '#' + str(int(sheet.cell(rows,3).value)))
                        disp_text = str(int(sheet.cell(rows,3).value))+'-'+text_format_translate(sheet.cell(rows,0).value)
                        new_image(file_name, 296, 50, disp_text,color=(0, 255, 0, 0), show_image=False)
            f.write('};\r')
			
			
 
 
if '__main__' == __name__:
    #new_image(100, 50, '你好1你好2你好3你好4', show_image=True)
    #new_image_with_file('image_data.txt')
    read_excel()
    #text_format_translate('你好 ~！@￥……*（）{}【】，。？')
