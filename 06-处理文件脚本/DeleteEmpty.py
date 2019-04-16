#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys

def delete_gap_dir(dir):
	if os.path.isdir(dir):
		for d in os.listdir(dir):
			delete_gap_dir(os.path.join(dir, d))

		if not os.listdir(dir):
			os.rmdir(dir)
			print('移除空目录: ' + dir)

if __name__=='__main__':
	if(len(sys.argv)>1):
		root_dir = sys.argv[1]
	
	delete_gap_dir(root_dir)
	print(u'删除完毕')