#!/usr/bin/python
# -*- coding: utf-8 -*-
# 删除指定路径的.DS_Store文件
import os
import sys
import string

# --------------------------.DS_Store
def del_DS_Store(path):
	# shell命令查找.DS_Store文件
	os.system(r'find %s -name .DS_Store' %path)
	
	for root, dirs, files in os.walk(path):
		for name in files:
			
			if string.find(name, 'DS_Store') != -1:
				os.remove(os.path.join(root, name))
				print ('删除文件: ' + os.path.join(root, name))
	print '-'*80

# if name.endswith(".tmp"):
# if name.startswith(".DS_"):

# --------------------------Thumbs.db
def del_Thumbs_db(path):
	# shell命令查找Thumbs.db文件
	os.system(r'find %s -name Thumbs.db' %path)
	
	for root, dirs, files in os.walk(path):
		for name in files:
			if string.find(name, 'Thumbs') != -1:
				os.remove(os.path.join(root, name))
				print ('删除文件: ' + os.path.join(root, name))
	
if __name__ == '__main__':
	if(len(sys.argv)>1):
		root_dir = sys.argv[1]

	del_DS_Store(root_dir)
	del_Thumbs_db(root_dir)
	print(u'删除完毕')