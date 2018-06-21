#!/usr/bin/python
#coding=utf-8

print('----------1-------')
try:
#	print(num)
	open('xxx.txt')
except (NameError, IOError), e:
	print('报错了')
	print(e)
print('----------2-------')


#def add(a, b):
#	print('%d+%d=%d'%(a, b, a+b))
#
#add(11, 22)
#
#lam = lambda a, b:'%d+%d=%d'%(a, b, a+b)
#res = lam(2, 4)
#print(res)

#a = input('the firset string:');
#print(a)



