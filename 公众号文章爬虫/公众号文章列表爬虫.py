# -*- coding: utf-8 -*-
import requests
import time
import json
import random


# 目标url
url = "https://mp.weixin.qq.com/cgi-bin/appmsg"

# 使用Cookie，跳过登陆操作
headers = {
  "Cookie": "###",#此处为F12获取的cookie
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
}

"""
需要提交的data
以下个别字段是否一定需要还未验证。
注意修改yourtoken,number
number表示从第number页开始爬取，为5的倍数，从0开始。如0、5、10……
token可以使用Chrome自带的工具进行获取
fakeid是公众号独一无二的一个id，等同于后面的__biz
"""
data = {
    "token": 123456,#此处为F12获取的token
    "lang": "zh_CN",
    "f": "json",
    "ajax": "1",
    "action": "list_ex",
    "begin": 0,
    "count": "5",
    "query": "",
    "fakeid": "MzAxMDA4NjgyOA==",
    "type": "9",
}

for i in range(196,263):
    data['begin'] = i * 5
    # 使用get方法进行提交
    content_json = requests.get(url, headers=headers, params=data).json()
    # 返回了一个json，里面是每一页的数据
    with open("./data.json", "a",encoding = 'utf8') as f:
        for item in content_json["app_msg_list"]:
        # 提取每页文章的标题及对应的url
                f.write(item['title'])
                f.write("\n")
                f.write(json.dumps(item["link"]))
                f.write("\n")
    print("已进行到第{}页".format(i + 1))
    time.sleep(60 + random.randrange(0,5))