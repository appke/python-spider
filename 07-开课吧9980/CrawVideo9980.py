# -*- coding:utf-8 -*-
import requests
import os, sys, time
import re
import m3u8
from Crypto.Cipher import AES
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
        self.down_url = 'http://student.kaikeba.com/course/82/study/4615'


        self.session = requests.Session()
        self.headers = {
            'Origin': 'http://student.kaikeba.com',
            'Referer': str(self.down_url), #获得key必须要
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }


    def main(self):
        # ---------------------------------------------------- 下载m3u文件 ---- 暂时手动下载 2019-04-10.m3u
        # self.down_m3u(url?)


        # ---------------------------------------------------- 最后删除加密的ts、破解的ts、m3u、key文件
        # self.clear_ts_file()  

        # ---------------------------------------------------- 先得到key文件
        # self.get_key() 

        # ---------------------------------------------------- 再下载所有的ts文件
        # alter_param = 'cd12-ccd1-2'
        # # alter_param = 'cd12-c120'
        # alter_param = 'cd15-c120-1'
        # self.down_ts_all(alter_param)


        # ---------------------------------------------------- 破解所有的ts ？？？会出错的，解码了DS_Store文件？
        # self.del_DS_Store(self.down_path)
        # self.decrypt_all_ts() 


        # ---------------------------------------------------- 合并文件，转为mp4
        # self.del_DS_Store(self.decrypt_path)
        # self.concat_ts()




# -----------------------------------------------------------------
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
    def down_ts_all(self, alter_param):
        base_url = 'https://{}.play.bokecc.com/flvs/7488FF1B7810DE53/{}/'.format(alter_param, self.down_date)

        m3u8_obj = self.get_m3u()
        uri_list = m3u8_obj.segments
        for key in uri_list:
            down_url = base_url + key.uri
            self.kaiKeBaBlock(down_url)


    def kaiKeBaBlock(self, down_url):
        index = re.search(r'video=(\d*)', down_url).group(1) 
        filename = index.zfill(4)

        resp = self.session.get(down_url, headers=self.headers)
        with open(r'{}.ts'.format(filename), 'wb') as f:
            f.write(resp.content)
        print('下载完成-----第{}段'.format(index))
        time.sleep(0.2)

# -----------------------------------------------------------------
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
        for fname in file_list:
            self.decrypt_single_ts(fname, key, iv)
    
    
    def decrypt_single_ts(self, file_name, key, iv):
        raw = open(file_name, 'rb').read()
        data = raw

        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        plain_data = cipher.decrypt(data)

        open('{0}/{1}'.format(self.decrypt_path, file_name), 'wb').write(plain_data)
        print('file: ' + file_name + '\tsucceed!')


# -----------------------------------------------------------------
    def concat_ts(self): 
        # 指定输出文件名称
        output_file = os.path.join(self.final_path, '{}.mp4'.format(self.down_date))
        # 使用ffmpeg将ts合并为mp4
        os.chdir(self.decrypt_path)
        print("正在合并\t{}.ts文件 ··········".format(self.down_date))
        os.system('cat *.ts > %s.ts'%(self.down_date))
        command = 'ffmpeg -i "%s.ts" -acodec copy -vcodec copy -absf aac_adtstoasc %s'%(self.down_date, output_file)
        # 指行命令
        os.system(command)
        print("最后转换成 {}.mp4\t完成！".format(self.down_date))



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
        os.remove(key_path)
        os.remove(m3u_path)

        print(key_path + "，清理完成！")
        print(m3u_path + "，清理完成！")


    def del_DS_Store(self, path):
        # shell命令查找.DS_Store文件
        os.system(r'find %s -name .DS_Store' %path)
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.find('DS_Store') != -1:
                    os.remove(os.path.join(root, name))
                    print ('删除文件: ' + os.path.join(root, name))
        print('-'*80)



craw = CrawVideo9980()
craw.main()