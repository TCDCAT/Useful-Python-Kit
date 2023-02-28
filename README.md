##export_translated.py
#脚本作用：导出多个语言的strings.xml到excel表格中
#使用方法：自行增加、删除、修改res_*_string的路径即可，默认导出res_cn_string对应的strings.xml的所有翻译语料，并且根据key添加其它语种的翻译

##find_strings_untranslated.py
#脚本作用：对比A string.xml，导出B string.xml没有的key和对应的string
#使用方法：根据脚本运行提示输入即可，需要使用python3运行

##import_string_excel_2_xml.py
#脚本作用：将excel中的翻译增量导入到string.xml中
#使用方法：根据脚本运行提示输入即可，需要使用python3运行
#注意事项：
#1.待导入的翻译资源需要是xlsx格式,xlsx格式参考Arabic.xlsx，需要注意
#   *第一列为strings.xml中的key，第四列为需要导入的翻译语料所在列，二三列为参考翻译
#2.使用python3运行脚本
#3.导入属于增量导入，会保留xml中的原有资源
