import requests
from urllib.parse import urlencode

def get_one_page(cityId, keyword):
	

	param = {
		'cityId': cityId, 	# 搜索城市
		'kw': keyword, 	# 职位
		'pageSize': '90',
		'kt': '3',
	}
	

	headers = {
		'Accept': 'application/json, text/plain, */*',
		'Referer': 'https://sou.zhaopin.com',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
	}

	url = 'https://fe-api.zhaopin.com/c/i/sou?' + urlencode(param)

	print('url----', url)
	resp = requests.get(url, headers=headers)
	print(resp.text)


def parse_one_page(html):
	pass

def main(city, keyword, page, region):
	pass




if __name__ == '__main__':
	get_one_page('765', 'NLP')



