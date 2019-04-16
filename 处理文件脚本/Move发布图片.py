#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import shutil


class ChangeName:
	def __init__(self):
		reload(sys) 
		sys.setdefaultencoding('utf-8')
		
	def main(self):

		root = sys.argv[1]
		# 查找商品图片
		skuList= os.listdir(root)
		for ii in skuList:
			# 测试存在图片库
			skuDir = os.path.join(root, ii)
			print skuDir
			
			fileList = os.listdir(skuDir)
			for fileName in fileList:
				print os.path.join(skuDir, fileName)
				# 把后缀变成小写
				files = os.path.splitext(fileName)
				changeName =os.path.splitext(files[0])[0] +files[1].lower()
				dest = os.path.join(u'/Users/mgbook/Desktop/发布商品图片11/', changeName)

				# 移动图片
				shutil.copy(os.path.join(skuDir, fileName), dest)
				
		
	
bn = ChangeName()
bn.main()