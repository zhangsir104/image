import configparser


def get_spider_conf(conf_file, conf_option, conf_name):
    conf = configparser.RawConfigParser()
    conf.read(conf_file)
    result = conf.get(conf_option, conf_name)
    return result
