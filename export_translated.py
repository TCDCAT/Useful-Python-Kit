#!/usr/bin/env python
# encoding: utf-8

#————————Note————————
#脚本作用：导出多个语言的strings.xml到excel表格中
#使用方法：自行增加、删除、修改res_*_string的路径即可，默认导出res_cn_string对应的strings.xml的所有翻译语料，并且根据key添加其它语种的翻译

import os, sys, getopt
import xml.dom.minidom
import subprocess
# import xlsxwriter
import xlwt
from xml.dom.minidom import Node

res_ru_string="/Users/hanwen/workspace/twinkle_nature/app/src/main/res/values-ru/strings.xml"
res_cn_string="/Users/hanwen/workspace/twinkle_nature/app/src/main/res/values-zh-rCN/strings.xml"
res_cn_tw_string="/Users/hanwen/workspace/twinkle_nature/app/src/main/res/values-zh-rTW/strings.xml"
res_ja_string="/Users/hanwen/workspace/twinkle_nature/app/src/main/res/values-ja/strings.xml"
res_en_string="/Users/hanwen/workspace/twinkle_nature/app/src/main/res/values/strings.xml"

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

# 导出所有语言文本
def export_xml():
    doc_ru = xml.dom.minidom.parse(res_ru_string)
    doc_en = xml.dom.minidom.parse(res_en_string)
    doc_ja = xml.dom.minidom.parse(res_ja_string)
    doc_cn = xml.dom.minidom.parse(res_cn_string)

    strings_ru = doc_ru.getElementsByTagName('string')
    strings_en = doc_en.getElementsByTagName('string')
    strings_ja = doc_ja.getElementsByTagName('string')
    strings_cn = doc_cn.getElementsByTagName('string')

    column_key = 0
    column_cn = 1
    column_en = 2
    column_ru = 3
    column_ja = 4
    # workbook = xlsxwriter.Workbook('find_strings_untranslated.xlsx', encoding ='utf-8') # 建立文件
    # worksheet = workbook.add_worksheet() # 建立sheet， 可以work.add_worksheet('employee')来指定sheet名，但中文名会报UnicodeDecodeErro的错误
    wb = xlwt.Workbook(encoding ='utf-8')
    worksheet = wb.add_sheet('Sheet1', True)

    worksheet.write(0,column_key,'key')
    worksheet.write(0,column_cn,'中文')
    worksheet.write(0,column_en,'英文')
    worksheet.write(0,column_ru,'俄文')
    worksheet.write(0,column_ja,'日文')

    line = 1

    for string_cn in strings_cn:
        name = string_cn.getAttribute('name')
        text_cn = getText(string_cn.childNodes)
        text_en = ' '
        text_ja = ' '
        text_ru = ' '
        for string_ru in strings_ru:
            if string_ru.getAttribute('name') == name:
                text_ru = getText(string_ru.childNodes)
                break
        for string_en in strings_en:
            if string_en.getAttribute('name') == name:
                text_en = getText(string_en.childNodes)
                break
        for string_ja in strings_ja:
            if string_ru.getAttribute('name') == name:
                text_rja= getText(string_ja.childNodes)
                break
        worksheet.write(line, column_key, name)
        worksheet.write(line, column_cn, text_cn)
        worksheet.write(line, column_en, text_en)
        worksheet.write(line, column_ja, text_ja)
        worksheet.write(line, column_ru, text_ru)
        line = line+1

    wb.save('多语言翻译语料集合.xlsx')
if __name__ == '__main__':
    export_xml()
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
    # else
    #     usage()