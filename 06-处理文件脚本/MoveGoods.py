#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import shutil



class ChangeName:
	
	def __init__(self):
		reload(sys) 
		sys.setdefaultencoding('utf-8')
		# 存在的商品
		self.currentList = []
		self.goodsCount = 0
		# 获得字典数据
		execfile(u'上传商品222.py')
		print len(self.goodsTuples)
		
	def main(self):
#		/Users/mgbook/Desktop/上传图片-已处理
#		
		root = u'/Users/mgbook/Desktop/上传商品-分批次'
		# 查找商品图片
		mainSkuList= os.listdir(root)
		for ii in mainSkuList:
			# 鲜食、干货目录
			mainSkuDir = os.path.join(root, ii)
			skuList = os.listdir(mainSkuDir)
			print len(skuList)
							
			for jj in skuList:
				# 商品目录
				skuDir = os.path.join(mainSkuDir, jj)
				
				for goods in self.goodsTuples:
					if jj == goods[0] or jj[:jj.find("_")] == goods[2]:
						# 将当前文件夹copy到桌面
						print skuDir
						dest = os.path.join(u'/Users/mgbook/Desktop/发布商品图片/', jj)
#						shutil.copytree(skuDir, dest)
						shutil.move(skuDir, dest)
						
						self.currentList.append(jj)
						self.goodsCount = self.goodsCount + 1
						
		# ----------------列出有图片的商品
		print len(self.currentList)
#		for ti in self.goodsTuples:
#			if ti[0] in self.currentList:
#				print '有'
#			else:
#				print '没有'

bn = ChangeName()
bn.main()