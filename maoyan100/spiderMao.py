import json
import requests, re
from requests.exceptions import RequestException
from multiprocessing import Pool

# 获取网页
def get_one_page(url):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        return None

# 解析网页
def parse_one_page(html):
    pattern = re.compile(r'<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?'
                         +'integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)

    # 格式化一下
    for item in items:
        # 构造一个字典
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }

def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        # 字典形式，转成字符串形式
        f.write(json.dumps(content, ensure_ascii=False)+'\n')


def main(offset):
    url = r'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        # print(item)
        write_to_file(item)


if __name__ == '__main__':
    # for i in range(10):
        # main(i*10)
    pool = Pool()
    # 数组中每个元素拿出来，当做前面函数的参数
    pool.map(main, [i*10 for i in range(10)])
