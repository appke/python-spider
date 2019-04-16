#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import shutil

class ChangeName:
	
	def __init__(self):
		reload(sys) 
		sys.setdefaultencoding('utf-8')
		# 已经存在的商品
		self.currentList = []
		self.goodsCount = 0
		# 获得字典数据
#		execfile(u'上传商品.py')
#		print len(self.goodsTuples)
		
	def main(self):
#		/Users/mgbook/Desktop/上传图片-已处理
		oldRoot = u'/Users/mgbook/Desktop/上传图片-已处理'
		# 已存在的商品图片
		mainSkuList = os.listdir(oldRoot)
		for ii in mainSkuList:
			skuList = os.listdir(os.path.join(oldRoot, ii))
			for jj in skuList:
				# 具体目录
				self.currentList.append(jj)
		
		newRoot = u'/Users/mgbook/Pictures/1214剩下商品/鲜食#熟食、面包'
		# 新文件夹中商品
		newSkuList= os.listdir(newRoot)
		for ii in newSkuList:
			if ii in self.currentList:
				# 重复商品目录
				print ii
				doubleDir = os.path.join(newRoot, ii)
				dest = os.path.join(u'/Users/mgbook/Pictures/重复商品/', ii)
				# 移动文件夹
				shutil.move(doubleDir, dest)
				
						
bn = ChangeName()
bn.main()
