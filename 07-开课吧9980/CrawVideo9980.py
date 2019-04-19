# -*- coding:utf-8 -*-
import requests
import os, sys, time
import re
import m3u8
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from binascii import unhexlify

class CrawVideo9980:
    def __init__(self):
        self.final_path = os.path.join(sys.path[0], 'FINAL')
        if not os.path.exists(self.final_path):
            os.makedirs(self.final_path)

        self.down_path = os.path.join(sys.path[0], 'DOWN')
        if not os.path.exists(self.down_path):
            os.makedirs(self.down_path)
        os.chdir(self.down_path)

        self.decrypt_path = os.path.join(sys.path[0], 'DECRYPT')
        if not os.path.exists(self.decrypt_path):
            os.makedirs(self.decrypt_path)

        # 下载那一天的
        self.down_date = '2019-01-30'
        self.down_url = 'http://student.kaikeba.com/course/103/study/4847'


        self.session = requests.Session()
        self.headers = {
            'Origin': 'http://student.kaikeba.com',
            'Referer': str(self.down_url),
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }


    def down_m3u(self, url):
        # resp = self.session.get(url, headers=self.headers)
        # print(resp.content)
        pass

    def get_m3u(self):
        m3u8_obj = m3u8.load('../{}.m3u'.format(self.down_date))
        return m3u8_obj


    def get_key(self):
        m3u8_obj = self.get_m3u()
        key_uri = m3u8_obj.keys[0].uri

        print("key_uri :" + key_uri)
        resp = self.session.get(key_uri, headers=self.headers)
        print(resp.content)
        with open(r'../{}.key'.format(self.down_date), 'wb') as f:
            f.write(resp.content)


# -----------------------------------------------------------------
    def down_ts_all(self):
        m3u8_obj = self.get_m3u()
        uri_list = m3u8_obj.segments

        for key in uri_list:
            key_url = key.uri
            self.kaiKeBaBlock(key_url)


    def kaiKeBaBlock(self, key_url):
        index = re.search(r'video=(\d*)', key_url).group(1)
        start_name = re.search(r'^(.*)-', key_url).group(1)
        print('开始下载-----第{}段'.format(index))
        base_url = 'https://cd12-ccd1-2.play.bokecc.com/flvs/7488FF1B7810DE53/{}/'.format(self.down_date)
        url = base_url + key_url

        resp = self.session.get(url, headers=self.headers)
        with open(r'{}-{}.ts'.format(start_name, index), 'wb') as f:
            f.write(resp.content)
        time.sleep(2)


# -----------------------------------------------------------------
    def chage_fileName(self):
        file_list = os.listdir(self.down_path)
        # 缺失的前面补0
        for file in file_list:
            names = file.split('-')
            newName = names[1].zfill(7)
            os.rename(file, newName)
        print("文件名修改完成！")



    def decrypt_all_ts(self): 
        # 读取ts文件夹下所有的ts文件
        file_list = os.listdir(self.down_path)
        # 对文件进行排序
        file_list.sort()
        file_sort = [filename for filename in file_list]

        m3u8_obj = self.get_m3u()
        iv_str = m3u8_obj.keys[0].iv
        print(iv_str)

        iv = bytes.fromhex(iv_str[2:])
        key = open('../{}.key'.format(self.down_date), 'rb').read()

        # AES-128解密
        for fname in file_sort:
            self.decrypt_single_ts(fname, key, iv)
    
    
    def decrypt_single_ts(self, file_name, key, iv):
        raw = open(file_name, 'rb').read()
        data = raw #raw[16:]
        aesObjc = AES.new(key, AES.MODE_CBC, iv)
        plain_data = aesObjc.decrypt(data)

        open('{0}/{1}'.format(self.decrypt_path, file_name), 'wb').write(plain_data)
        print('file: ' + file_name + '\tsucceed!')


# -----------------------------------------------------------------
    def concat_ts(self):
        # 指定输出文件名称
        output_file = os.path.join(self.final_path, '{}.mp4'.format(self.down_date))
        # 使用ffmpeg将ts合并为mp4
        os.chdir(self.decrypt_path)
        os.system('cat *.ts > %s.ts'%(self.down_date))
        command = 'ffmpeg -i "%s.ts" -acodec copy -vcodec copy -absf aac_adtstoasc %s'%(self.down_date, output_file)
        # 指行命令
        os.system(command)
        print("文件合并，转为mp4完成！")
    

    def clear_ts_file(self):
        down_list = os.listdir(self.down_path)
        for fname in down_list:
            os.remove(self.down_path+ '/' +fname)
        print(self.down_path + "，清理完成！")

        decrypt_list = os.listdir(self.decrypt_path)
        for fname in decrypt_list:
            os.remove(self.decrypt_path+ '/' +fname)
        print(self.decrypt_path + "，清理完成！")

        base_path = os.path.split(self.final_path)[0]
        m3u_path = os.path.join(base_path, "%s.m3u"%(self.down_date))
        key_path = os.path.join(base_path, "%s.key"%(self.down_date))
        os.remove(m3u_path)
        os.remove(key_path)

        print(m3u_path + "，清理完成！")
        print(key_path + "，清理完成！")

    def del_DS_Store(self, path):
        # shell命令查找.DS_Store文件
        os.system(r'find %s -name .DS_Store' %path)
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.find('DS_Store') != -1:
                    os.remove(os.path.join(root, name))
                    print ('删除文件: ' + os.path.join(root, name))
        print('-'*80)
    

    def main(self):
        # ---------------------------------------------------- 下载m3u文件 ---- 暂时手动下载 2019-04-10.m3u
        # self.down_m3u(url?)
        
        # ---------------------------------------------------- 先得到key文件
        # self.get_key()

        # ---------------------------------------------------- 下载所有的ts文件
        # self.down_ts_all()

        # ---------------------------------------------------- 修改文件名，必须修改！
        # self.del_DS_Store(self.down_path)
        # self.chage_fileName() 

        # ---------------------------------------------------- 破解所有的ts
        # ValueError: Data must be padded to 16 byte boundary in CBC mode
        # self.decrypt_all_ts()


        # ---------------------------------------------------- 合并文件，转为mp4
        # self.del_DS_Store(self.decrypt_path)
        # self.concat_ts()


        # ---------------------------------------------------- 最后删除加密的ts、破解的ts、m3u、key文件
        # self.clear_ts_file()



    # def get_ip_list(self):
    #     print("正在获取代理列表...")
    #     url = 'http://www.xicidaili.com/nn/'
    #     html = requests.get(url=url, headers=self.headers).text
    #     soup = BeautifulSoup(html, 'lxml')
    #     ips = soup.find(id='ip_list').find_all('tr')
    #     ip_list = []
    #     for i in range(1, len(ips)):
    #         ip_info = ips[i]
    #         tds = ip_info.find_all('td')
    #         ip_list.append(tds[1].text + ':' + tds[2].text)
    #     print("代理列表抓取成功.")
    #     return ip_list


    # def get_random_ip(self,ip_list):
    #     print("正在设置随机代理...")
    #     proxy_list = []
    #     for ip in ip_list:
    #         proxy_list.append('http://' + ip)
    #     proxy_ip = random.choice(proxy_list)
    #     proxies = {'http': proxy_ip}
    #     print("代理设置成功.")
    #     return proxies

    

    # def run(self):
    #     print("Start!")
    #     start_time = time.time()
    #     os.chdir(self.down_path)
        # html = requests.get(self.url,  headers=self.headers).text
        # print(html)

        # bsObj = BeautifulSoup(html, 'lxml')
        # realAdr = bsObj.find('video', class_="vsc-initialized").find("source")['src']
        # print(realAdr)

        # realAdr = 'https://cd12-ccd1-2.play.bokecc.com/flvs/7488FF1B7810DE53/2019-04-10/1CD46E78FE2AB8F29C33DC5901307461-90.m3u8?t=1555068309&key=854F21AA3AACF4D7D91CEBB9A4B181EE&tpl=10&tpt=112'
        # print(requests.get(realAdr, headers=self.headers).content)

        # duration = bsObj.find('meta', {'property': "video:duration"})['content'].replace("\"", "")
        # limit = int(duration) // 10 + 3

        # # ip_list = self.get_ip_list()
        # # proxies = self.get_random_ip(ip_list)

        # uriList = self.get_uri_from_m3u8(realAdr)
        # print(uriList)

        # i = 1   # count
        # for key in uriList:
        #     if i%50==0:
        #         print("休眠10s")
        #         time.sleep(10)
        #     if i%120==0:
        #         print("更换代理IP")
        #         proxies = self.get_random_ip(ip_list)
        #     try:
        #         resp = requests.get(key.uri, headers = self.headers, proxies=proxies)
        #     except Exception as e:
        #         print(e)
        #         return
        #     if i < 10:
        #         name = ('clip00%d.ts' % i)
        #     elif i > 100:
        #         name = ('clip%d.ts' % i)
        #     else:
        #         name = ('clip0%d.ts' % i)
        #     with open(name,'wb') as f:
        #         f.write(resp.content)
        #         print('正在下载clip%d' % i)
        #     i = i+1
        # print("下载完成！总共耗时 %d s" % (time.time()-start_time))
        # print("接下来进行合并……")
        # os.system('copy/b %s\\*.ts %s\\%s.ts' % (self.down_path, self.final_path, self.name))
        # print("合并完成，请您欣赏！")


        # y = input("请检查文件完整性，并确认是否要删除碎片源文件？(y/n)")
        # if y=='y':
        #     files = os.listdir(self.down_path)
        #     for filena in files:
        #         del_file = self.down_path + '\\' + filena
        #         os.remove(del_file)
        #     print("碎片文件已经删除完成")
        # else:
        #     print("不删除，程序结束。")


craw = CrawVideo9980()
craw.main()


