from urllib.parse import urlencode

from util.configure import get_spider_conf
from util.util import image_to_md5
from util import constants
from util.image_obj import ImageObj

import requests


baidu_web_url = get_spider_conf(constants.SPIDERCONF, 'baidu', 'baidu_web_url')
my_headers = get_spider_conf(constants.SPIDERCONF, 'baidu', 'my_headers')
word = get_spider_conf(constants.SPIDERCONF, 'baidu', 'word')
last_paginator = get_spider_conf(constants.SPIDERCONF, 'baidu', 'last_paginator')
paginator = get_spider_conf(constants.SPIDERCONF, 'baidu', 'paginator')

# 图片对象
img = ImageObj()


class ImageBaiduSpider(object):
    def __init__(self):
        self.web_url = baidu_web_url
        self.headers = my_headers
        self.word = word
        self.last_paginator = int(last_paginator)
        self.paginator = int(paginator)

    def get_web_url(self, offset):
        params = {"tn": "resultjson_com",
                   "logid": "12086572661949889640",
                   "ipn": "rj",
                   "ct": "201326592",
                   "is": "",
                   "fp": "result",
                   "queryWord": self.word,
                   "cl": "2",
                   "lm": "-1",
                   "ie": "utf-8",
                   "oe": "utf-8",
                   "adpicid": "",
                   "st": "",
                   "z": "",
                   "ic": "",
                   "hd": "",
                   "latest": "",
                   "copyright": "",
                   "word": self.word,
                   "s": "",
                   "se": "",
                   "tab": "",
                   "width": "",
                   "height": "",
                   "face": "",
                   "istype": "",
                   "qc": "",
                   "nc": "1",
                   "fr": "",
                   "expermode": "",
                   "force": "",
                   "cg": "star",
                   "pn": offset * 30,
                   "rn": "30",
                   "gsm": "1e",
                   "1609071177455": ""
                       }
        web_url = self.web_url + urlencode(params)
        # print(web_url)
        return web_url

    def save_image_to_dir(self, img_url):
        img_page = requests.get(img_url, headers=eval(self.headers)).content
        img_md5 = image_to_md5(img_page)
        # print(img_md5)
        with open('image_spider/baidu_spider/image_file/{}.jpg'.format(img_md5), 'wb') as f:
            f.write(img_page)
        # print(img_page)

    def save_image_to_db(self, img_url):
        img_page = requests.get(img_url, headers=eval(self.headers)).content
        img_md5 = image_to_md5(img_page)

        # 图片信息存入图片对象
        img.url = img_url
        img.page = img_page
        img.md5 = img_md5
        return img

    def get_image(self, web_url):
        try:
            response = requests.get(web_url, headers=eval(self.headers))
            data_list = response.json().get('data', None)
            # print(data_list)
            img_list = []
            if data_list:
                for data in data_list:
                    img_url = data.get('thumbURL')
                    if img_url:
                        #self.save_image_to_dir(img_url)
                        img = self.save_image_to_db(img_url)
                        img_list.append(img)
                        #print(img_url)
            return img_list
        except ConnectionError as e:
            print('erro', e)

    def run_image_baidu_spider(self):
        for offset in range(self.last_paginator, self.paginator):
            web_url = self.get_web_url(offset)
            img_list = self.get_image(web_url)
            yield img_list


# if __name__ == '__main__':
#     image = ImageBaiduSpider()
#     image.run_image_baidu_spider()
