import requests
import m3u8
from Crypto.Cipher import AES
from binascii import unhexlify


# m3u8_obj = m3u8.load('../20190414.m3u')
# uriList = m3u8_obj.segments
# print(m3u8_obj.target_duration)
# m3u8_obj = m3u8.load('20190417.m3u')
# uriList = m3u8_obj.segments
# key = m3u8_obj.keys[0]
# print(key.uri, key.method, key.iv)


# https://p.bokecc.com/servlet/hlskey?info=DDC3B2F65E54D1509C33DC5901307461&t=1555583107&key=6E8DE94B955A0CF3F2021CBCF4B4B82C AES-128 0xDDC3B2F65E54D1509C33DC5901307461


# def get_Key(url):
#     headers = {
#         'Referer': 'http://student.kaikeba.com/course/103/study/5930',
#         'Origin': 'http://student.kaikeba.com',
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
#     }
#     resp = requests.get(url, headers=headers)
#     print(resp.content)
#     with open(r'20190417.key', 'wb') as f:
#         f.write(resp.content)






def decrypt_single_ts(file_name, key_path, iv_str):
    raw = open(file_name, 'rb').read()
    iv = bytes.fromhex(iv_str)
    data = raw #raw[16:]
    key = open(key_path, 'rb').read()

    plain_data = AES.new(key, AES.MODE_CBC, iv).decrypt(data)
    open('decode_ts/{0}'.format(file_name), 'wb').write(plain_data)
    print('file:' + file_name + '\tsucceed!')



# print(unhexlify("ae98961dd802f860ae9b67dd75136a18"))
# print(bytes.fromhex("66EF7E894DDF835B9C33DC5901307461"))
# print(unhexlify("66EF7E894DDF835B9C33DC5901307461"))
# print('8B7D40EE4D490E6FD4BCB28D03EE2EE8'.encode())

# 8B7D40EE4D490E6FD4BCB28D03EE2EE8
# from Crypto import Random
# key = b'Sixteen byte key'
# iv = Random.new().read(AES.block_size)
# cipher = AES.new(key, AES.MODE_CFB, iv)
# msg = iv + cipher.encrypt(b'Attack at dawn')
# print(msg)
# print(len(iv))

# url = 'https://p.bokecc.com/servlet/hlskey?info=DDC3B2F65E54D1509C33DC5901307461&t=1555584538&key=650D7766ECC81AF3DC22A8D86AFBFD34'
# get_Key(url)

decrypt_single_ts("0002.ts", '2019-01-21.key', "624FBC0CD9A3EE6F9C33DC5901307461")



# # 解密并合并一个m3u8文件
# def decrypt_single(m3u8_path):
#     fp = open(m3u8_path, 'r')
#     lines = fp.readlines()
#     fp.close()
#     pat_uri = r"URI=\"(.+)\"" #搜索URI的模式
#     pat_iv = r"IV=0x(\w+)" #搜索IV的模式
#     regex_uri = re.compile(pat_uri)
#     regex_iv = re.compile(pat_iv)
#     datas = b''
#     for idx in range(2, len(lines), 3):
#         if lines[idx] is not None and "ENDLIST" not in lines[idx]:
#             key = regex_uri.search(lines[idx])[1].strip()
#             iv = regex_iv.search(lines[idx])[1].strip()
#             ts = lines[idx + 2].strip()
#             datas += decrypt_single_ts(key, iv, ts)
#     return datas
