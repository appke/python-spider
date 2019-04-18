
# coding: utf-8

# 1 已知字符串:
# info = '<a href="http://www.baidu.com">baidu</a>'
# 用正则模块提取出网址："http://www.baidu.com" 和 链接文本:"baidu"
# 
# 2 字符串："one1two2three3four4" 用正则处理，输出 "1234"
# 
# 3 已知字符串：text = "JGood is a handsome boy, he is cool, clever, and so on..." 查找所有包含'oo'的单词。
# 
# 4 为什么在unix里，grep后面的正则有些时候要加引号，有些时候不需要。

# In[2]:


import re
info = '<a href="http://www.baidu.com">baidu</a>'
print(re.search(r'<a href="(.*?)">', info).group(1))
print(re.search(r'<a href="(.*?)">(.*?)</a>', info).group(2))


# In[17]:


text2 = 'one1two2three3four4'
print(re.sub(r'\D', '', text2))
print(re.split(r'\d', text2))
print(re.split(r'\D', text2))


# In[11]:


text3 = "JGood is a handsome boy, he is cool, clever, and so on..."
print(re.findall(r'\w*oo\w*',text3))


# 4. 正则表达式里有特殊含义的字符，需要加分号

# 已知字符串：
# info = 'test,&nbsp;url("http://www.baidu.com")&,dddddd "="" <svg></svg><path></path><img src="http://www.baidu.com">ininnnin<img src="http://www.dd.com">'
# 
# 要求完成下面2个小功能：
# 1.1 关闭[img]标签
# 1.2 将url()中的["]转为[']
# 
# 最后结果字符串：
# "test,&nbsp;url('http://www.baidu.com')&,dddddd "="" <svg></svg><path></path><img src="http://www.baidu.com"></img>ininnnin<img src="http://www.dd.com"></img>"
