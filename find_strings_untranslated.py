#!/usr/bin/env python
# encoding: utf-8

#————————Note————————
#脚本作用：对比A string.xml，导出B string.xml没有的key和对应的string
#使用方法：根据脚本运行提示输入即可，需要使用python3运行

import os, sys, getopt
import xml.dom.minidom
import subprocess
# import xlsxwriter
import xlwt
from xml.dom.minidom import Node


# map_lan_res = {'zh':res_cn_string, 'en':res_en_string, 'ru':res_ru_string, 'ja':res_ja_string}
# map_lan_desc = {'zh':'Chinese', 'en':'English', 'ru':'Russian', 'ja':'Japanese'}

# # 检查资源文件列表
# res_string_files=[res_en_string, res_cn_string]

# # Java调用字符串资源列表
# find_string_called_by_java='''find . -name .repo -prune -o -name .git -prune -o -type f -name "*\.java" -print0 | xargs -0 grep --color -n -o 'R.string[0-9A-Za-z_.-]\+'|awk -F':' '{print $3}'|sort|uniq|xargs echo'''

# def _check_string_res(path):
#     """检查字符串资源调用情况

#     :path: TODO
#     :returns: TODO

#     """
#     os.chdir(path)
#     if not os.path.exists(Axml):
#         return

#     # 输出提示
#     print "\n### Processing Project: %s ..\n" % path

#     # 获得字符串资源调用情况
#     find_string_called_by_java_array = subprocess.Popen(find_string_called_by_java, shell=True, stdout=subprocess.PIPE).stdout.read().split(' ')

#     # 逐个检查资源文件（目前检查中文、英文）
#     for res_string_file in res_string_files:
#         print ">>> Checking %s file .." % res_string_file

#         # 解析xml文件，并保存已有资源到 names_had
#         doc = xml.dom.minidom.parse(res_string_file)
#         strings = doc.getElementsByTagName('string')
#         names_had = []
#         for string in strings:
#             name = string.getAttribute('name')
#             names_had.append(name)

#         # 逐个检查被调用的字符串资源，不存在此资源时报Warning
#         for check in find_string_called_by_java_array:
#             c=check[9:].strip()
#             if c not in names_had:
#                 print "  - Warning: string name '%s' not found!!!" % c

# def usage(exitval=0):
#     print "\nUsage: %s project_dir1 project_dir2 ..\n" % sys.argv[0]

stringxml_all = ""   #包含全部翻译的文档
# stringxml_all_refer = res_en_string  
stringxml_to_check = ""    #需要检查遗漏翻译的文档，和stringxml_all中的语料通过string的name属性进行对比，检查哪些没有翻译


def readUserInput():
    global stringxml_all
    global stringxml_to_check
    stringxml_all = input("请输入包含全部翻译的string.xml文件绝对路径:")
    stringxml_to_check = input("请输入需要检查遗漏翻译的string.xml文件绝对路径:")


def findStringsUntranslated():
    global stringxml_all
    global stringxml_to_check
    print("————开始查找遗漏翻译————")

    #待翻译文档，和doc_trans对比，检查哪些没有翻译
    dom_to_check = xml.dom.minidom.parse(stringxml_to_check)
    #对比文档，检查有哪些没有翻译，一般是中文xml
    dom_all = xml.dom.minidom.parse(stringxml_all)
    # dom_all_refer = xml.dom.minidom.parse(stringxml_all_refer)
    
    strings_to_check = dom_to_check.getElementsByTagName('string')
    strings_all = dom_all.getElementsByTagName('string')
    # strings_all_refer = dom_all_refer.getElementsByTagName('string')

    column_key = 0
    column_to_translate = 3
    # column_refer_real = 2
    # column_trans = 2
    
    # workbook = xlsxwriter.Workbook('find_strings_untranslated.xlsx', encoding ='utf-8') # 建立文件
    # worksheet = workbook.add_worksheet() # 建立sheet， 可以work.add_worksheet('employee')来指定sheet名，但中文名会报UnicodeDecodeErro的错误
    wb = xlwt.Workbook(encoding ='utf-8')
    worksheet = wb.add_sheet('Sheet1', True)

    worksheet.write(0,column_key,'name')
    worksheet.write(0,column_to_translate,'string_to_translate')

    line = 1

    for string_all in strings_all:
        name = string_all.getAttribute('name')
        
        hasTranslated = 0
        for string_to_check in strings_to_check:
            if string_to_check.getAttribute('name') == name:
                hasTranslated = 1
                break
        if hasTranslated == 0:
            # nodeText_refer_real = ''
            # for string_refer_real in strings_all_refer:
            #     if string_refer_real.getAttribute('name') == name:
            #         nodeText_refer_real = getText(string_refer_real.childNodes)
            #         break
            nodeText = getText(string_all.childNodes)
            print("found:{0} {1}".format(name, nodeText))
            worksheet.write(line, column_key, name)
            worksheet.write(line, column_to_translate, nodeText)
            # worksheet.write(line, column_refer_real, nodeText_refer_real)
            line = line+1
            #跳过那些不包含中文的语料，无需翻译
            # if hasChinese(nodeText):
            #     worksheet.write(line, column_key, name)
            #     worksheet.write(line, column_refer, nodeText)
            #     worksheet.write(line, column_refer_real, nodeText_refer_real)
            #     line = line+1
    wb.save('string_to_translate.xlsx')
    print("————查找完成，所有未翻译的文件已经导出到当前目录下的string_to_translate.xlsx文件————")

def hasChinese(string):
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print "参数输入错误，请按照顺序输入参考语言和待翻译语言，语言列表如下\ncn(chinese) ja(japanes) en(english) ru(russian)"
    #     return
    readUserInput()
    findStringsUntranslated()
    # if len(sys.argv) == 1:
    #     if os.path.isfile(Axml):
    #         _check_string_res(os.path.abspath('.'))
    #     else:
    #         usage()
    # elif len(sys.argv) > 1:
    #     for path in sys.argv[1:]:
    #         if os.path.isdir(path):
    #             _check_string_res(os.path.abspath(path))
    #         else:
    #             print "### %s Not a directory, ignored." % path
    # else:
    #     usage()


