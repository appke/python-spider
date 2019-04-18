import json
import requests

def xima(albumId, page):
	url = 'https://www.ximalaya.com/revision/play/album?albumId={}&pageNum={}&sort=-1&pageSize=30'.format(albumId, page+1)
	# 'https://www.ximalaya.com/revision/album/getTracksList?albumId=20261281&pageNum=1'
	print(url)

	# 模拟浏览器
	headers = {
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
	}

	resp = requests.get(url, headers=headers)
	str = resp.content.decode()
	# 把字符串变成字典
	result = json.loads(str)

	for track in result['data']['tracksAudioPlay']:
		src = track['src']
		name = track['trackName']
		with open('mp4/{}.m4a'.format(name), 'ab') as f:
			music = requests.get(src, headers=headers)
			f.write(music.content)
		print('下载完成---'+name)
		break

def crawAll(albumId):
	for page in range(3):
		xima(albumId, page)


# 获取专辑的id
def crawOneBook():
	
	url = 'https://www.ximalaya.com/revision/rank/v1/album/getCategoryRankPage?code=yinyue&pageNum=1&pageSize=100'
	headers = {
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
	}
	resp = requests.get(url, headers=headers)
	str = resp.content.decode()
	result = json.loads(str)

	for album in result['data']['albums']:
		albumId = album['id']
		crawAll(albumId)



if __name__ == "__main__":
	# crawOneBook()
	# 连岳专辑
	crawAll('20261281')
