import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse,urlencode,parse_qs

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
}

titles = []
urls = []

with open("data.json",'r',encoding='utf8') as f:
    for i,data in enumerate(f.readlines()):
        if i % 2 == 0:
            titles.append(data)
        else:
            url = urlparse(data[1:-2])
            query = url.query
            query = parse_qs(query)
            query = "__biz=" + "".join(query['__biz']) + "&mid=" + "".join(query['mid']) + "&idx=" + "".join(query['idx']) + "&sn=" + "".join(query['sn'])
            url = "http://mp.weixin.qq.com/s?" + query
            urls.append(url)
with open('索引.txt','w',encoding='utf8') as index:
    for i,data in enumerate(titles):
        try:
            res = requests.get(urls[i], headers=headers).content
            soup = BeautifulSoup(res,'html.parser')
            with open('article\\' + str(i) + '.txt','w',encoding='utf8') as resault:
                resault.write(soup.find('h2').text.strip() + '\n\n')
                for child in soup.find('div',class_='rich_media_content').find_all('p'):
                    text = child.text.strip()
                    if text == "":
                        continue
                    resault.write(text + '\n')
        except Exception as e:
            index.write(str(i) + "\t错误\n")
            print('在第%d页出现错误:%s' % (i + 1,e))
            continue
        index.write(str(i) + "\t" + data.strip() + "\n")
        print("已进行到第%d篇文章" % (i + 1))
        index.flush()
        time.sleep(3)