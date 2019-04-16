#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import re


class PrintName:
	
	def __init__(self):
		reload(sys) 
		sys.setdefaultencoding('utf-8')
		# 存在的商品
		self.currentList = []
		self.goodsCount = 0
		# 获得字典数据
		execfile(u'上传商品.py')
#		print len(self.goodsTuples)
		
	def main(self):
		
		root = u'/Users/mgbook/Desktop/上传图片-已处理'
		# 查找商品图片
		mainSkuList= os.listdir(root)
		for ii in mainSkuList:
			# 鲜食、干货目录
			mainSkuDir = os.path.join(root, ii)
			skuList = os.listdir(mainSkuDir)
			for jj in skuList:
				# 商品目录
				skuDir = os.path.join(mainSkuDir, jj)
				self.goodsCount = self.goodsCount + 1
				self.currentList.append(jj)
				
#		print len(self.currentList)
#				for goods in self.goodsTuples:
#					if jj == goods[0] or jj[:jj.find("_")] == goods[2]:
						
		# ----------------列出有图片的商品
		count = 0
		isDisplay = False
		for tt in self.goodsTuples:
			isDisplay = False
			for gg in self.currentList:
				
				if tt[0] == gg or tt[2] == gg[:gg.find("_")]:
					print '已上架'
					isDisplay = True
					count = count + 1
					break
			if isDisplay == False:
				print '未上架'
				
		print count
pn = PrintName()
pn.main()