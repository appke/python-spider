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


# 根据商品链接爬
#class JD:
#
#	def __init__(self):
#		
#		reload(sys) 
#		sys.setdefaultencoding('utf-8')
#		
#		
#		self.session = requests.Session()
#		self.argv1 = sys.argv[1]
#
#		# 获取商品信息
#		if len(sys.argv) >= 2:
#			# 执行python文件
# 			execfile(self.argv1)
#		else:
#			print 'Lack Of Parameter. Exit.'
#			exit()
#			
#	
#	def main(self):
#
#		for i in range(len(self.keywords)):
#			self.keyword = self.keywords[i][0]
#			self.tcount = 1
#			self.dcount = 1
#
#			print 'Begin To Crawl: ' + self.keyword
#			
#			# 直接爬图片
#			mainSku = self.argv1[0:len(self.argv1)-3]
#			imgPath = r'jd/'+ mainSku +'/' + self.keyword
#			if os.path.exists(r'jd'):
#				if os.path.exists(imgPath):
#					shutil.rmtree(imgPath)
#				# 递归创建，没有s~上一个文件夹不存在报错
#				os.makedirs(imgPath)
#			else:
#				print 'Not Exist Img Dir. Exit.'
#				exit()
#
#			productUrl = self.keywords[i][1];
#			productResponse = self.session.get(productUrl)
#			print productResponse.url
#			productSoup = BeautifulSoup(productResponse.text, 'lxml')
#			productImgs = productSoup.find('div', id='spec-list').select('img')
#			
#			skuId = re.search(r'https?://(.*?)/(.*?)\.html', productResponse.url).group(2)
#			
#			for productImg in productImgs:
#				imgUrl = 'https:' + re.sub(r'/\w*jfs/', '/jfs/', re.sub(r'/n\d/', '/n12/', productImg.get('src')))
#				print imgUrl
#				imgResponse = self.session.get(imgUrl)
#				fileName = skuId + '_TITLE_' + ('0' if self.tcount<10 else '') + str(self.tcount) + imgUrl[-4:]
#				
#				self.tcount = self.tcount + 1
#				open(imgPath + r'//' + fileName, 'wb').write(imgResponse.content)
#
#			#print productResponse.text
#
#			# --------------- 下载详情图片 -----------------
#			try:
#				mainSkuId = re.search(r'mainSkuId=(\d*)', productResponse.text).group(1)
#			except Exception as e:
#				mainSkuId = skuId
#			print 'mainSkuId=' + mainSkuId
#			
#			
#			contentUrl = 'https://cd.jd.com/description/channel?skuId='+skuId+'&mainSkuId='+mainSkuId
#			print contentUrl
#			contentResponse = self.session.get(contentUrl)
#
#			contentImgs = re.findall(r'//img.*?\.(?:jpg|png)', contentResponse.text)
#			for contentImg in contentImgs:
#				imgUrl = contentImg.encode("utf-8")
#				if imgUrl[0:5] != r'https':
#					imgUrl = r'https:' + imgUrl
#				print imgUrl
#				imgResponse = self.session.get(imgUrl)
#				
#				fileName = skuId + r'_DETAIL_' + (r'0' if self.dcount<10 else r'') + str(self.dcount) + imgUrl[-4:]
#				
#				self.dcount = self.dcount + 1
#				open(imgPath + r'//' + fileName, r'wb').write(imgResponse.content)
#
#			print 'End To Crawl: ' + self.keyword
#
#jd = JD()
