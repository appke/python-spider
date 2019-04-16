#!/usr/bin/python
# -*- coding: utf-8 -*-


#GOODS308_DETAIL_01.jpg
#文件校验失败，失败原因：文件名称错误。文件名：GOODS173_TITLE_01.JPG.jpg
#文件校验失败，失败原因：文件名称错误。文件名：GOODS173_DETAIL_03.JPG.jpg
import os

fileList = ['GOODS173_TITLE_01.JPG.jpg', 'GOODS173_DETAIL_03.jpg', 'GOODS173_detail_03.JPG.jpg', 'GOODS173_DETAIL_03.JPG.PNG']

for fileName in fileList:
	files = os.path.splitext(fileName)
	changeName = os.path.splitext(files[0])[0].upper() +files[1].lower()

	print changeName