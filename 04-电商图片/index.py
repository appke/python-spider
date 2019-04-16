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

		if len(sys.argv) >= 2:
			self.keyword = sys.argv[1]
		else:
			print 'Lack Of Parameter. Exit.'
			exit()

	def main(self):

		for i in range(len(self.keywords)):
			self.keyword = self.keywords[i]
			imgPath = 'GoodsPic//img//非食3-个护//' + self.keyword
			if os.path.exists('img'):
				if os.path.exists(imgPath):
					shutil.rmtree(imgPath)
				os.mkdir(imgPath)
			else:
				print 'Not Exist Img Dir. Exit.'
				exit()

			print 'Begin To Crawl: ' + self.keyword

			print 'Begin To Crawl In JD: ' + self.keyword

			searchUrl = 'https://search.jd.com/Search?keyword='+ urllib.quote(self.keyword) + '&enc=utf-8&pvid=53b9c13c3b164cfa82f8337013d7b2a8'
			print 'SearchUrl: ' + searchUrl
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
				print 'Crawl Failed. JD Not Exist This Product.'
			else:
				productResponse = self.session.get(productUrl)
				productSoup = BeautifulSoup(productResponse.text, 'lxml')
				productImgs = productSoup.find('div', id='spec-list').select('img')
				for productImg in productImgs:
					imgUrl = 'https:' + re.sub(r'/\w*jfs/', '/jfs/', re.sub(r'/n\d/', '/n12/', productImg.get('src')))
					print imgUrl
					imgResponse = self.session.get(imgUrl)
					fileName = re.search('\w*.jpg|\w*.png', imgUrl).group()
					open(imgPath + '//' + fileName, 'wb').write(imgResponse.content)

			if jdFind is not True:

				print 'Begin To Crawl In Tianmao: ' + self.keyword

				searchUrl = 'https://list.tmall.com/search_product.htm?q='+ urllib.quote(self.keyword) + '&type=p&spm=a220m.1000858.a2227oh.d100&from=.list.pc_1_searchbutton'
				print 'SearchUrl: ' + searchUrl
				searchResponse = self.session.get(searchUrl)
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
					print 'Crawl Failed. Tianmao Not Exist This Product.'
				else:
					productResponse = self.session.get(productUrl)
					productSoup = BeautifulSoup(productResponse.text, 'lxml')
					productImgs = productSoup.find('ul', id='J_UlThumb').select('img')
					for productImg in productImgs:
						imgUrl = 'https:' + re.sub(r'.jpg.*.jpg$', '.jpg', productImg.get('src'))
						print imgUrl 					
						imgResponse = self.session.get(imgUrl)
						fileName = re.search('(.*)/(.*.jpg)|(.*)/(.*.png)', imgUrl).group(2)
						open(imgPath + '//' + fileName, 'wb').write(imgResponse.content)

			 if jdFind is True or tmFind is True:
			 	print '有'
			 else :
			 	print '没有'

			print 'End To Crawl: ' + self.keyword

jd = JD()
jd.main()