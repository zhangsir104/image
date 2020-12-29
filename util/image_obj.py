class ImageObj(object):
    def __init__(self):
        self.page = None   # 图片二进制
        self.md5 = None    # 图片md5值， 用md5加密图片二进制生成的字符串，可用于区分图片
        self.url = None    # 图片url
        self.height = None  # 图片高
        self.wight = None    # 图片宽
        self.quality = None  # 图片质量