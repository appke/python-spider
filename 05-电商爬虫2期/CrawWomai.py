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

#https://detail.1688.com/offer/549798086124.html?spm=a261b.8781817.pinpai-list.9.MUIwfF
# 根据商品链接爬
class JD:

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
			self.keyword = self.keywords[i][0]
			self.tcount = 1
			self.dcount = 1

			print 'Begin To Crawl: ' + self.keyword
			
			# 直接爬图片
			mainSku = self.argv1[0:len(self.argv1)-3]
			imgPath = r'womai/'+ mainSku +'/' + self.keyword
			if os.path.exists(r'womai'):
				if os.path.exists(imgPath):
					shutil.rmtree(imgPath)
				# 递归创建，没有s~上一个文件夹不存在报错
				os.makedirs(imgPath)
			else:
				print 'Not Exist Img Dir. Exit.'
				exit()

			productUrl = self.keywords[i][1];
			productResponse = self.session.get(productUrl)
			print productResponse.url
			productSoup = BeautifulSoup(productResponse.text, 'lxml')
			productImgs = productSoup.find('div', class_='items').select('img')
			
			
			for productImg in productImgs:
				imgUrl = productImg.get('jqimg')
				print imgUrl
				imgResponse = self.session.get(imgUrl)
				fileName = 'womai' + '_TITLE_' + ('0' if self.tcount<10 else '') + str(self.tcount) + imgUrl[-4:]
				
				self.tcount = self.tcount + 1
				open(imgPath + r'/' + fileName, 'wb').write(imgResponse.content)


#			# --------------- 下载详情图片 -----------------#
			contentImgs = productSoup.find('div', class_='content').select('img')
			
			for contentImg in contentImgs:
				imgUrl = contentImg.get('src')
				if not imgUrl.startswith('http'):
					continue
				print imgUrl

				imgResponse = self.session.get(imgUrl)
				fileName = 'womai' + r'_DETAIL_' + (r'0' if self.dcount<10 else r'') + str(self.dcount) + imgUrl[-4:]
				self.dcount = self.dcount + 1
				open(imgPath + r'/' + fileName, r'wb').write(imgResponse.content)

			print 'End To Crawl: ' + self.keyword

jd = JD()
jd.main()