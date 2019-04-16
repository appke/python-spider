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

class TM:

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

			headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
			print 'Begin To Crawl: ' + self.keyword
			
			
			# ------------ 搜索 有结果才创建文件夹
			# imgPath = r'tianmao/非食1/' + self.keyword
			mainSku = self.argv1[0:len(self.argv1)-3]
			imgPath = r'tm/'+ mainSku +'/' + self.keyword
			print imgPath
			if os.path.exists(r'tm'):
				if os.path.exists(imgPath):
					shutil.rmtree(imgPath)
				os.makedirs(imgPath)
			else:
				print 'Not Exist Img Dir. Exit.'
				exit()
				
			# ------------ 发送请求
			productUrl = self.keywords[i][1]
			productResponse = self.session.get(productUrl, headers=headers)
			productSoup = BeautifulSoup(productResponse.text, 'lxml')
			productImgs = productSoup.find('ul', id='J_UlThumb').select('img')
			# 没必要了
			skuId = re.search(r'id=(\d*)', productUrl).group(1)
			print "skuId=" + skuId
			
			# 下载_TITLE_图片	
			for productImg in productImgs:
				imgUrl = 'https:' + re.sub(r'.jpg.*.jpg$', r'.jpg', productImg.get('src'))
				print imgUrl
				imgResponse = self.session.get(imgUrl)
				fileName = r'TM' + '_TITLE_' + str(self.tcount).zfill(2) + imgUrl[-4:]
				self.tcount = self.tcount + 1
				open(imgPath + r'/' + fileName, 'wb').write(imgResponse.content)

			
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
				fileName = r'TM' + r'_DETAIL_' + str(self.dcount).zfill(2) + imgUrl[-4:]
				
				self.dcount = self.dcount + 1
				open(imgPath + r'/' + fileName, r'wb').write(imgResponse.content)

			print 'End To Crawl: ' + self.keyword
			

tm = TM()
tm.main()