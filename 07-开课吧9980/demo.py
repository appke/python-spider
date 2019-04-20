# print "hello"


import requests


def dowm_single_ts(url):
    
    headers = {
        'Origin': 'http://student.kaikeba.com',
        'Referer': 'http://student.kaikeba.com/course/103/study/5555',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    resp = requests.get(url, headers = headers)
    print(resp)


    with open(r'9999.ts', 'wb') as f:
        f.write(resp.content)


if __name__ == '__main__':
    url = 'https://cd12-c120.play.bokecc.com/flvs/7488FF1B7810DE53/2019-03-17/FF4310CEB687C1A79C33DC5901307461-90.ts?video=3&t=1555745679&key=00B29068E594774FF976C18381E6B7C7&tpl=10&tpt=112'
    dowm_single_ts(url)


https://cd12-c120.play.bokecc.com/flvs/7488FF1B7810DE53/2019-03-17/FF4310CEB687C1A79C33DC5901307461-90.ts?video=3&t=1555745679&key=00B29068E594774FF976C18381E6B7C7&tpl=10&tpt=112
https://cd12-ccd1-2.play.bokecc.com/flvs/7488FF1B7810DE53/{}/'.format(self.down_date)