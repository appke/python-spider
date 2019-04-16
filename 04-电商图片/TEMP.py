#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import re

#s=r'\tt'
#print(s)
#
#s=r'\.t'
#print(s)
#
# 
#s='\tt'
#print(s)

#productUrl = 'https://detail.tmall.com/item.htm?id=531313624326&skuId=3457532432656&user_id=272715291&cat_id=2&is_b=1&rn=f75335747c65de2813a323234d6a4213'
#skuId = re.search(r'skuId=(\d*)&', productUrl).group(1)
#print "skuId=" + skuId


html='''
<div class="panel">
	<div class="panel-heading">
		<h4>Hello</h4>
	</div>
	<div class="panel-body">
		<ul class="list" id="list-1">
			<li class="element">Foo</li>
			<li class="element">Bar</li>
			<li class="element">Jay</li>
		</ul>
		<ul class="list list-small" id="list-2">
			<li class="element">Foo</li>
			<li class="element">Bar</li>
		</ul>
	</div>
</div>
'''

#html = '''<a href="http://example.com/elsie" class="sister" id="link">Elsie</a>'''


#from bs4 import BeautifulSoup
#soup = BeautifulSoup(html, 'lxml')
#print(soup.select('.panel .panel-heading'))
#print(soup.select('ul li'))
#print(soup.select('#list-2 .element'))
#print(type(soup.select('ul')[0]))

#from bs4 import BeautifulSoup
#soup = BeautifulSoup(html, 'lxml')
#for li in soup.select('li'):
#	print(li.get_text())


from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
for ul in soup.select('ul'):
	print(ul['id'])
	print(ul.attrs['id'])

#print soup.find(id='link')
##	- `<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>`
#print soup.find(id='link').get('href')
#	- `http://example.com/elsie`




  
