#!/usr/bin/python
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

class TEST:

	def __init__(self):
		reload(sys) 
		sys.setdefaultencoding('utf-8')
		
		self.session = requests.Session()
		self.argv1 = sys.argv[1]

		# 获取商品信息
		if len(sys.argv) >= 2:
			# 执行python文件
 			execfile(self.argv1)
		else:
			print 'Lack Of Parameter. Exit.'
			exit()


	def main(self):

#		contentUrl = 'https://cd.jd.com/description/channel?skuId=2358318&mainSkuId=2358318'
#		print contentUrl
#		contentResponse = self.session.get(contentUrl)
#		contentImgs = re.findall(r'//.*?\.jpg|//.*?\.png|//.*?.gif', contentResponse.text)
#		contentImgs = re.findall(r'//.*?\.jpg|//.*?.png|//.*?.gif', contentResponse.text)

#		print re.findall(r'//.*?\.(?:jpe?g|png|gif)', contentResponse.text)
#		print re.findall(r'\.jpg|\.png|\.gif', contentResponse.text)
		

#		contentImgs = re.findall(r'//.*\.(?:jpg|png|gif)', contentResponse.text)
#		print contentImgs
		
#		open('productList.txt', 'wb').write(contentResponse.text)
						
#		print re.search('(*)\.py$', self.argv1).group(1)
		
		searchUrl = 'https://list.tmall.com/search_product.htm?q='+ urllib.quote('浪莎简约隐形袜') + '&type=p&spm=a220o.0.a2227oh.d100&from=.detail.pc_1_searchbutton'
		print 'SearchUrl: ' + searchUrl
		searchResponse = self.session.get(searchUrl)
		searchResponse.encoding = 'utf-8'
		searchSoup = BeautifulSoup(searchResponse.text, 'lxml')

#		print searchSoup.findAll()
		print searchSoup.find('div', id='J_ItemList').find('p', class_='productTitle').find('a').get('href')
				
		exit()
		
		
		
		print 'End To Crawl: ' + self.keyword
		
		imgPath = r'jd//'+ mainSku +'//' + self.keyword
		if os.path.exists(r'jd'):
			if os.path.exists(imgPath):
				shutil.rmtree(imgPath)
			# 递归创建，没有s~上一个文件夹不存在报错
			os.makedirs(imgPath)
		else:
			print 'Not Exist Img Dir. Exit.'
			exit()

			

test = TEST()
test.main()