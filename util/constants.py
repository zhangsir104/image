import os

SPIDERCONF = os.path.join(os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'conf'), 'spider.conf')
print(SPIDERCONF)