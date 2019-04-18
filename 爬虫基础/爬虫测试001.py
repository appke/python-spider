
# coding: utf-8

# In[16]:


import urllib.request
response = urllib.request.urlopen('http://httpbin.org/get')
print(response.read().decode('utf-8'))


# In[19]:


import urllib.parse
import urllib.request

data = bytes(urllib.parse.urlencode({'word':'hello', 'age':'23'}), encoding='utf-8')
response = urllib.request.urlopen('http://httpbin.org/post', data=data)
print(response.read())


# In[15]:


# import requests
# response = requests.get(r'https://www.baidu.com')
# response.encoding = 'utf-8'
# print(response.text)

