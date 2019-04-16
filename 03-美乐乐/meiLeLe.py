# -*- coding: UTF-8 -*-

import requests
import json
import re
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
import urllib
import sys
import math


#http://www.meilele.com/expr.html?area=%E5%8D%8E%E4%B8%9C%E5%9C%B0%E5%8C%BA&page=1


def init():
	reload(sys) 
	sys.setdefaultencoding('utf-8')

def getURL(area, page, index):
	pages = range(int(page))
	for i in pages:
		url = 'http://www.meilele.com/expr.html?area='+area+'&page='+str(i+1)
		# 只适合第一个——华东地区
#		getAreaPageHome(url)
		getAreaPageOther(url, index)
		

def getAreaPageHome(url):
	# 下载
	res = requests.get(url)
	# 查找
	soup = BeautifulSoup(res.text, 'lxml')
	
	store_list = soup.find('div', class_='area_menu_content').find('div', class_='store_list clearfix')
#	print type(store_list)
	txtAreaList = store_list.find_all('div', class_='Right txtArea')
	for item in txtAreaList:
		print item.get_text()


def getAreaPageOther(url, index):
	# 下载
	res = requests.get(url)

	# 查找
	soup = BeautifulSoup(res.text, 'lxml')
	attrs={'style':r'display: block;'}
	store_list = soup.find('div', class_='area_menu_content').find_all('div', class_='store_list clearfix')
#	print len(store_list)
#	find('div', attrs={'style':'display: block;'})
#	
	
	current_store_list = store_list[index]
	txtAreaList = current_store_list.find_all('div', class_='Right txtArea')
	for item in txtAreaList:
		print item.get_text()
	

def main():
	init()
#	getURL(u'华东地区', '9', 0)
#	getURL(u'华南地区', '7', 1)
#	getURL(u'华中地区', '2', 2)
#	getURL(u'华北地区', '7', 3)
#	getURL(u'西南地区', '5', 4)
#	getURL(u'西北地区', '1', 5)
#	getURL(u'东北地区', '1', 6)
	
	
	
#	getURL(u'华南地区', '7')
#	print type(int('2'))
#	getAreaPage(u'http://www.meilele.com/expr.html?area=华东地区&page=1')

if __name__ == "__main__":
	main()

