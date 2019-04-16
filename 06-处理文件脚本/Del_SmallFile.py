#!/usr/bin/python
# -*- coding: utf-8 -*-
# 删除指定路径的 小文件
import os
import sys

def del_smallFile(path):	
	for root, dirs, files in os.walk(path):
		for name in files:
			filepath = os.path.join(root, name)
			# mac上按1000算的
			filesize = os.path.getsize(filepath) / 1000.0
#			print filepath, filesize
#			25
			if filesize < 1:
				os.remove(filepath)
				print ('删除文件: ' + filepath)

# if name.endswith(".tmp"):
# if name.startswith("."):

if __name__ == '__main__':
	if(len(sys.argv)>1):
		root_dir = sys.argv[1]

	del_smallFile(root_dir)
	print(u'删除完毕')