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
import string
import time

# 根据商品链接爬
class CrawAll:

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
			

	def crawJD(self, productUrl):
		# 直接爬图片
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
		
		time.sleep(1.0)
		productResponse = self.session.get(productUrl)
		print productResponse.url
		productSoup = BeautifulSoup(productResponse.text, 'lxml')
		productImgs = productSoup.find('div', id='spec-list').select('img')
		
		skuId = re.search(r'https?://(.*?)/(.*?)\.html', productResponse.url).group(2)
		
		for productImg in productImgs:
#			//img14.360buyimg.com/n5/jfs/t4234/359/1442024427/383479/329c8f43/58c22be0N31ba3c73.jpg
			imgUrl = 'https:' + re.sub(r'/\w*jfs/', '/jfs/', re.sub(r'/n\d/', '/n12/', productImg.get('src')))
			print imgUrl
			imgResponse = self.session.get(imgUrl)
			fileName = skuId + '_TITLE_' + ('0' if self.tcount<10 else '') + str(self.tcount) + imgUrl[-4:]
			
			self.tcount = self.tcount + 1
			open(imgPath + r'/' + fileName, 'wb').write(imgResponse.content)

		#print productResponse.text

		# --------------- 下载详情图片 -----------------
		try:
			mainSkuId = re.search(r'mainSkuId=(\d*)', productResponse.text).group(1)
		except Exception as e:
			mainSkuId = skuId
		print 'mainSkuId=' + mainSkuId
		
		contentUrl = 'https://cd.jd.com/description/channel?skuId='+skuId+'&mainSkuId='+mainSkuId
		print contentUrl
		contentResponse = self.session.get(contentUrl)

		contentImgs = re.findall(r'//img.*?\.(?:jpg|png)', contentResponse.text)
		for contentImg in contentImgs:
			imgUrl = contentImg.encode("utf-8")
			if imgUrl[0:5] != r'https':
				imgUrl = r'https:' + imgUrl
			print imgUrl
			imgResponse = self.session.get(imgUrl)
			
			fileName = skuId + r'_DETAIL_' + (r'0' if self.dcount<10 else r'') + str(self.dcount) + imgUrl[-4:]
			
			self.dcount = self.dcount + 1
			open(imgPath + r'/' + fileName, r'wb').write(imgResponse.content)
			
			
	def crawTM(self, productUrl):	
		headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
		# ------------ 搜索 有结果才创建文件夹
		# imgPath = r'tm/非食1/' + self.keyword
		mainSku = self.argv1[0:len(self.argv1)-3]
		imgPath = r'tm/'+ mainSku +'/' + self.keyword
		if os.path.exists(r'tm'):
			if os.path.exists(imgPath):
				shutil.rmtree(imgPath)
			os.makedirs(imgPath)
		else:
			print 'Not Exist Img Dir. Exit.'
			exit()
			
		# ------------ 发送请求
		productResponse = self.session.get(productUrl, headers=headers)
		print productResponse.url
		productSoup = BeautifulSoup(productResponse.text, 'lxml')
		productImgs = productSoup.find('ul', id='J_UlThumb').select('img')
		
		# 下载_TITLE_图片	
		for productImg in productImgs:
			imgUrl = re.search(r'//img.*?\.(?:jpg|png)', productImg.get('src')).group()
			if imgUrl[0:5] != 'https':
				imgUrl = 'https:' + imgUrl

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
		contentResponse = self.session.get(contentUrl, headers=headers)
		contentImgs = re.findall(r'//img.*?\.(?:jpg|png)', contentResponse.text)
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

	def crawTaoBao(self, productUrl):
					
			headers = {
				'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
				}

			# ------------ 搜索 有结果才创建文件夹
			# imgPath = r'tianmao/非食1/' + self.keyword
			mainSku = self.argv1[0:len(self.argv1)-3]
			imgPath = r'taobao/'+ mainSku +'/' + self.keyword
			if os.path.exists(r'taobao'):
				if os.path.exists(imgPath):
					shutil.rmtree(imgPath)
				os.makedirs(imgPath)
			else:
				print 'Not Exist Img Dir. Exit.'
				exit()
				
			# ------------ 发送请求
			productResponse = self.session.get(productUrl, headers=headers)
			print productResponse.url
			productSoup = BeautifulSoup(productResponse.text, 'lxml')
			productImgs = productSoup.find('ul', id='J_UlThumb').select('img')
			
			# 下载_TITLE_图片	
			for productImg in productImgs:
				# 淘宝店
				imgUrl = re.search(r'//.*?\.(?:jpg|png)', productImg['data-src']).group()
				
				if imgUrl[0:5] != 'https':
					imgUrl = 'https:' + imgUrl
				print imgUrl
				
				imgResponse = self.session.get(imgUrl)
				fileName = r'TB' + '_TITLE_' + str(self.tcount).zfill(2) + imgUrl[-4:]
				self.tcount = self.tcount + 1
				open(imgPath + r'/' + fileName, 'wb').write(imgResponse.content)
			

			# 淘宝继续下载
			# ---------------------- 下载详情图片 ----------------------
			# 详情页js路径
			try:
				contentUrl = re.search(r"location.protocol===.*?'(//.*?)'", productResponse.text).group(1)
				if not contentUrl.startswith('http'):
					contentUrl = 'http:' + contentUrl
				print 'contentUrl: ' + contentUrl
			except Exception as e:
				print "Not Find Picture Detail Page"

#			contentHeaders = {
#				'Host':'dsc.taobaocdn.com'
#				'Upgrade-Insecure-Requests':'1'
#				'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
#			}

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
				fileName = r'TB' + r'_DETAIL_' + str(self.dcount).zfill(2) + imgUrl[-4:]
				self.dcount = self.dcount + 1
				open(imgPath + r'/' + fileName, r'wb').write(imgResponse.content)

	def craw1688(self, productUrl):
		# 直接爬图片
		mainSku = self.argv1[0:len(self.argv1)-3]
		imgPath = r'1688/'+ mainSku +'/' + self.keyword
		if os.path.exists(r'1688'):
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
		productImgs = productSoup.find('div', id='dt-tab').select('img')
		
		
		for productImg in productImgs:
			imgUrl = re.sub(r'60x60\.', '', productImg.get('src'))
			print imgUrl
			imgResponse = self.session.get(imgUrl)
			fileName = '1688' + '_TITLE_' + ('0' if self.tcount<10 else '') + str(self.tcount) + imgUrl[-4:]
			
			self.tcount = self.tcount + 1
			open(imgPath + r'/' + fileName, 'wb').write(imgResponse.content)


		# --------------- 下载详情图片 -----------------#
		contentUrl = productSoup.find('div', id='desc-lazyload-container')['data-tfs-url']
		print contentUrl
		contentResponse = self.session.get(contentUrl)
		
		
		contentImgs = re.findall(r'https://cbu.*?\.(?:jpg|png)', contentResponse.text)
		for contentImg in contentImgs:
			imgUrl = contentImg.encode("utf-8")
			if imgUrl[0:5] != r'https':
				imgUrl = r'https:' + imgUrl
			print imgUrl
			
			if contentUrl != imgUrl:
				contentUrl = imgUrl
			else:
				continue
				
			imgResponse = self.session.get(imgUrl)
			fileName = '1688' + r'_DETAIL_' + (r'0' if self.dcount<10 else r'') + str(self.dcount) + imgUrl[-4:]
			self.dcount = self.dcount + 1
			open(imgPath + r'/' + fileName, r'wb').write(imgResponse.content)
		
	def crawWomai(self, productUrl):
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
		
	def main(self):
		for i in range(len(self.keywords)):
			self.keyword = self.keywords[i][0]
			self.tcount = 1
			self.dcount = 1

			print 'Begin To Crawl: ' + self.keyword
			productUrl = self.keywords[i][1]
			
			# 京东
			if string.find(productUrl, 'jd.com') != -1:
				self.crawJD(productUrl)
			# 天猫
			elif string.find(productUrl, 'tmall.com') != -1:
				self.crawTM(productUrl)
			elif string.find(productUrl, 'taobao.com') != -1:
				self.crawTaoBao(productUrl)
			elif string.find(productUrl, '1688.com') != -1:
				self.craw1688(productUrl)
			elif string.find(productUrl, 'womai.com') != -1:
				self.crawWomai(productUrl)

			else:
				print "不匹配---------------------" + self.keyword
				exit()
			print 'End To Crawl: ' + self.keyword


crawAll = CrawAll()
crawAll.main()