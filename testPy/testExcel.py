#!/usr/bin/python
#-*- coding: utf-8 -*-

#import csv
#
#with open('testd.csv') as f:
#	reader = csv.reader(f)
#	print  list(reader)
	
import csv
csvfile = file('csvtest.csv', 'wb')
writer = csv.writer(csvfile)
writer.writerow(['id', 'url', 'keywords'])
data = [
	('1', 'http://www.xiaoheiseo.com/', '小黑'),
	('2', 'http://www.baidu.com/', '百度'),
	('3', 'http://www.jd.com/', '京东')
]
writer.writerows(data)
csvfile.close()