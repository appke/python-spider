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
import time

class OneShop:

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
		for i in range(len(self.keywords)):
			self.keyword = self.keywords[i]
			self.tcount = 1
			self.dcount = 1

			print 'Begin To Crawl: ' + self.keyword
			
			searchUrl = 'http://search.yhd.com/c0-0/k'+ urllib.quote(self.keyword)
			print 'SearchUrl: ' + searchUrl
			searchResponse = self.session.get(searchUrl)
			searchSoup = BeautifulSoup(searchResponse.text, 'lxml')
			
			time.sleep(0.5)
			
			try:
				# productUrl = searchSoup.find('div', id='J_ItemList').find('p', class_='productTitle').find('a').get('href')
				productUrl = searchSoup.find('div', id='itemSearchList').find('a', class_="img").get('href')
			
				if productUrl[0:5] != 'https':
					productUrl = 'https:' + productUrl
				print 'ProductUrl: ' + productUrl
				
			except Exception as e:
				print 'Crawl Failed. Not Exist This Product.'
				#print '没有'
			else:
				# ------------ 搜索 有结果才创建文件夹
				mainSku = self.argv1[0:len(self.argv1)-3]
				imgPath = r'1号店/'+ mainSku +'/' + self.keyword
				print imgPath
				if os.path.exists(r'1号店'):
					if os.path.exists(imgPath):
						shutil.rmtree(imgPath)
					os.makedirs(imgPath)
				else:
					print 'Not Exist Img Dir. Exit.'
					exit()
					
				# ------------ 发送请求
				productResponse = self.session.get(productUrl)
				productSoup = BeautifulSoup(productResponse.text, 'lxml')
				# 找到 _TITLE_图片
				productImgs = productSoup.find('div', class_='mBox clearfix').select('img')
				
				# 下载_TITLE_图片	
				for productImg in productImgs:
					imgUrl = 'https://img13.360buyimg.com/n12/' + productImg.get('original_src')
					print imgUrl
					imgResponse = self.session.get(imgUrl)
					fileName = r'one' + '_TITLE_' + str(self.tcount).zfill(2) + imgUrl[-4:]
					self.tcount = self.tcount + 1
#					open(imgPath + r'/' + fileName, 'wb').write(imgResponse.content)

				
				# ---------------------- 下载详情图片 ----------------------
				# 详情页js路径
				try:
					contentUrl = re.search(r'"httpsDescUrl"\:"(//.*?)"}', productResponse.text).group(1)
					if contentUrl[0:5] != 'https':
						contentUrl = 'https:' + contentUrl
					print 'contentUrl: ' + contentUrl
				except Exception as e:
					print "Not Find Picture Detail Page"


				# 详情页请求结果
				contentResponse = self.session.get(contentUrl)
				contentImgs = re.findall(r'https://img.*?\.(?:jpg|png)', contentResponse.text)
				# 下载_DETAIL_图片
				for contentImg in contentImgs:
					imgUrl = contentImg.encode("utf-8")
					if imgUrl[0:5] != r'https':
						imgUrl = r'https:' + imgUrl
					print imgUrl
					
					imgResponse = self.session.get(imgUrl)
					fileName = r'one' + r'_DETAIL_' + str(self.dcount).zfill(2) + imgUrl[-4:]
					
					self.dcount = self.dcount + 1
					open(imgPath + r'/' + fileName, r'wb').write(imgResponse.content)

			print 'End To Crawl: ' + self.keyword
			

oneShop = OneShop()
oneShop.main()