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
#			self.id = self.keywords[i][0]
			self.tcount = 1
			self.dcount = 1

			print 'Begin To Crawl: ' + self.keyword

			searchUrl = 'https://search.jd.com/Search?keyword='+ urllib.quote(self.keyword) + '&enc=utf-8&pvid=53b9c13c3b164cfa82f8337013d7b2a8'
			print 'SearchUrl: ' + searchUrl
			searchResponse = self.session.get(searchUrl)
			searchResponse.encoding = 'utf-8'
			searchSoup = BeautifulSoup(searchResponse.text, 'lxml')

			try:
				productUrl = searchSoup.find('div', id='J_goodsList').find('li').find('a').get('href')
				if productUrl[0:5] != 'https':
					productUrl = 'https:' + productUrl
				print 'ProductUrl: ' + productUrl
				#print '有'
			except Exception as e:
				print 'Crawl Failed. Not Exist This Product.'
				#print '没有'
			else:
				
				# imgPath = r'jd//特殊//' + self.keyword
				mainSku = self.argv1[0:len(self.argv1)-3]
				imgPath = r'jd/'+ mainSku +'/' + self.keyword
				if os.path.exists(r'jd'):
					if os.path.exists(imgPath):
						shutil.rmtree(imgPath)
					# 递归创建，没有s~上一个文件夹不存在报错
					os.makedirs(imgPath)
				else:
					print 'Not Exist Img Dir. Exit.'
					exit()

				productResponse = self.session.get(productUrl)
				print productResponse.url
				productSoup = BeautifulSoup(productResponse.text, 'lxml')
				productImgs = productSoup.find('div', id='spec-list').select('img')
				
				skuId = re.search(r'https://(.*)/(.*).html', productResponse.url).group(2)
				print "skuId=" + skuId
				
				for productImg in productImgs:
					imgUrl = 'https:' + re.sub(r'/\w*jfs/', '/jfs/', re.sub(r'/n\d/', '/n12/', productImg.get('src')))
					print imgUrl
					imgResponse = self.session.get(imgUrl)
#					fileName = self.id + '_TITLE_' + ('0' if self.tcount<10 else '') + str(self.tcount) + imgUrl[-4:]
					fileName = skuId + '_TITLE_' + ('0' if self.tcount<10 else '') + str(self.tcount) + imgUrl[-4:]
					
					self.tcount = self.tcount + 1
					open(imgPath + r'//' + fileName, 'wb').write(imgResponse.content)

				#print productResponse.text

				# --------------- 下载详情图片 -----------------
				try:
					mainSkuId = re.search(r'mainSkuId=(\d*)', productResponse.text).group(1)
				except Exception as e:
					mainSkuId = skuId
				print mainSkuId
				
				
				contentUrl = 'https://cd.jd.com/description/channel?skuId='+skuId+'&mainSkuId='+mainSkuId
				print contentUrl
				contentResponse = self.session.get(contentUrl)
				# content = json.loads(contentResponse.text)
				# contentSoup = BeautifulSoup(content['content'], 'lxml')
				# print contentSoup.style

#			    要改进
				# //.*?\.(?:jpe?g|png|gif)
				contentImgs = re.findall(r'//.*?\.jpg|//.*?\.png|//.*?\.gif', contentResponse.text)
				for contentImg in contentImgs:
					imgUrl = contentImg.encode("utf-8")
					if imgUrl[0:5] != r'https':
						imgUrl = r'https:' + imgUrl
					print imgUrl
					imgResponse = self.session.get(imgUrl)
#					fileName = self.id + r'_DETAIL_' + (r'0' if self.dcount<10 else r'') + str(self.dcount) + imgUrl[-4:]
					fileName = skuId + r'_DETAIL_' + (r'0' if self.dcount<10 else r'') + str(self.dcount) + imgUrl[-4:]
					
					self.dcount = self.dcount + 1
					open(imgPath + r'//' + fileName, r'wb').write(imgResponse.content)

				# topDiv = productSoup.find('div', id='J-detail-pop-tpl-top-new')
				# if topDiv is not None:
				# 	topImgs = topDiv.select('img')
				# 	for topImg in topImgs:
				# 		imgUrl = topImg.get('src')
				# 		if imgUrl[0:5] != 'https':
				# 			imgUrl = 'https:' + imgUrl
				# 		print imgUrl
				# 		imgResponse = self.session.get(imgUrl)
				# 		fileName = re.search('\w*.jpg|\w*.png|\w*.gif', imgUrl).group()
				# 		open(imgPath + '//' + fileName, 'wb').write(imgResponse.content)

				# contentDiv = productSoup.find('div', id='J-detail-content')
				# print contentDiv
				# contentImgs = productSoup.find('div', id='J-detail-content').select('img')
				# print contentImgs
				# for contentImg in contentImgs:
				# 	imgUrl = contentImg.get('src')
				# 	if imgUrl is not None:
				# 		imgUrl = contentImg.get('src')
				# 	else:
				# 		imgUrl = contentImg.get('data-lazyload')
				# 	if imgUrl[0:5] != 'https':
				# 		imgUrl = 'https:' + imgUrl
				# 	print imgUrl
				# 	imgResponse = self.session.get(imgUrl)
				# 	fileName = re.search('\w*.jpg|\w*.png|\w*.gif', imgUrl).group()
				# 	open(imgPath + '//' + fileName, 'wb').write(imgResponse.content)

			print 'End To Crawl: ' + self.keyword

jd = JD()
jd.main()