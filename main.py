import os
import time
from multiprocessing import Process, Queue

from image_spider.baidu_spider.image_baidu_spider import ImageBaiduSpider
from image_db.img2mongodb.image2mgodb import image_to_mongodb

imagegspider = ImageBaiduSpider()


class ImageToDb(object):
    def __init__(self):
        self.queue = Queue()

    def producer(self):

        img_list = imagegspider.run_image_baidu_spider()
        if img_list:
            for i in img_list:
                # print(len(i))
                for img in i:
                    print(img)
                    self.queue.put(img)
                    print("{}成功放入队列".format(img.md5))

    def consumer(self):
        while True:
            if self.queue.empty():
                print('队列为空')
                time.sleep(10)
                if self.queue.empty():
                    break

            img = self.queue.get()
            print("{}成功从队列取出".format(img.md5))
            if img:
                image_to_mongodb(img)

    def run(self):
        pro_task = Process(target=self.producer)
        con_task = Process(target=self.consumer)
        pro_task.start()

        con_task.start()


if __name__ == '__main__':

    # 添加环境路径，后续写入配置文件
    env_path = os.environ['PATH']
    mydir = os.getcwd()
    os.environ['PATH'] = mydir + ';' + env_path

    ImageToDb().run()



