#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import re


class ChangeName:
	
	def __init__(self):
		reload(sys) 
		sys.setdefaultencoding('utf-8')
		# 存在的商品
#		self.currentList = []
#		self.goodsCount = 0
		# 获得字典数据
		execfile(u'上传商品222.py')
		print len(self.goodsTuples)
		
	def main(self):
		
		root = u'/Users/mgbook/Desktop/发布商品图片'
		count = 0
		# 查找商品图片
		skuList= os.listdir(root)
		for ii in skuList:
			# 测试存在图片库
			skuDir = os.path.join(root, ii)
			print skuDir
			
			fileList = os.listdir(skuDir)
			self.goodsID = '1000'
			# 1.找到文件对应的编码
			for goods in self.goodsTuples:
				if ii == goods[0] or ii[:ii.find("_")] == goods[2]:
					self.goodsID = goods[1]
					break
				
			# 逐个修改图片名字
			for oldName in fileList:
				# 商品目录
				names = oldName.split('_')
				names[0] = self.goodsID
				newName = '_'.join(names)
				os.rename(os.path.join(skuDir, oldName), os.path.join(skuDir, newName))

			count += 1
		print count
				
				
						
		# ----------------列出有图片的商品
#		for ti in self.goodsTuples:
#			if ti[0] in self.currentList:
#				print '有'
#			else:
#				print '没有'

bn = ChangeName()
bn.main()