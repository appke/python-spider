# -*- coding: UTF-8 -*-

import requests
import json
import re
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
import urllib
import sys
import os
import shutil

class JD:

	def __init__(self):

		self.session = requests.Session()

		# 获取商品信息
		if len(sys.argv) >= 2:
			# 执行python文件
 			execfile(sys.argv[1])
		else:
			print 'Lack Of Parameter. Exit.'
			exit()

	def main(self):

		for i in range(len(self.keywords)):
			self.keyword = self.keywords[i]
			
			# 先到京东查找
			searchUrl = 'https://search.jd.com/Search?keyword='+ urllib.quote(self.keyword) + '&enc=utf-8&pvid=53b9c13c3b164cfa82f8337013d7b2a8'
			
			searchResponse = self.session.get(searchUrl)
			searchResponse.encoding = 'utf-8'
			searchSoup = BeautifulSoup(searchResponse.text, 'lxml')

			jdFind = True
			try:
				productUrl = searchSoup.find('div', id='J_goodsList').find('li').find('a').get('href')
				if productUrl[0:5] != 'https':
					productUrl = 'https:' + productUrl
				print 'ProductUrl: ' + productUrl
			except Exception as e:
				jdFind = False

			# 到天猫查找
			if jdFind is not True:
				headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
				searchUrl = 'https://list.tmall.com/search_product.htm?q='+ urllib.quote(self.keyword)
				
				searchResponse = self.session.get(searchUrl,headers=headers)
				searchResponse.encoding = 'utf-8'
				searchSoup = BeautifulSoup(searchResponse.text, 'lxml')

				tmFind = True
				try:
					productUrl = searchSoup.find('div', id='J_ItemList').find('div').find('a').get('href')
					if productUrl[0:5] != 'https':
						productUrl = 'https:' + productUrl
					print 'ProductUrl: ' + productUrl
				except Exception as e:
					tmFind = False

			# 最后输出
			if jdFind is True or tmFind is True:
				print '有'
			else:
				print '没有'


jd = JD()
jd.main()