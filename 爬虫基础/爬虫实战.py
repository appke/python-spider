
# coding: utf-8

# In[24]:


from bs4 import BeautifulSoup
import lxml

html = '<input id="sessionId" class="hide" name="fp" value="877289787asvv6827y8bhsbh2989829894" type="hidden">'
soup = BeautifulSoup(html, 'html5lib')
fp = soup.select('input[name="fp"]')[0]
print(fp)


# In[2]:


from selenium import webdriver
browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
print(browser.page_source)
browser.close()


# In[7]:


from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
print(browser.get_cookies())
browser.add_cookie({'name': '穆良', 'domain': 'www.zhihu.com', 'value': 'germey'})
print(browser.get_cookies())
browser.delete_all_cookies()
# print(browser.get_cookies())

