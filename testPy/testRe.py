#!/usr/bin/python
#coding=utf-8 

#import csv
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

var = u'中华人民共和国中华人民共和国'
pattern = re.compile(u'中华(.*)共和国')

res = re.findall(pattern, var)

for item in res:
	print item
	
re.search(pattern, var)