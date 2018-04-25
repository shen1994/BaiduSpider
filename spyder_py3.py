# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 11:29:30 2017

@author: shenxinfeng
"""
'''
import sys
reload(sys)
sys.setdefaultencoding('utf8')
'''
import os
import re
import urllib
import urllib2
import json
import socket
import threading
# 设置超时
import time

timeout = 5
socket.setdefaulttimeout(timeout)

class Crawler:
    # 睡眠时长
    __time_sleep = 0.1
    __amount = 0
    __start_amount = 0
    __counter = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    # 获取图片url内容等
    # t 下载图片时间间隔
    def __init__(self, t=0.1):
        self.time_sleep = t

    # 保存图片
    def __save_image(self, rsp_data, word):
        
        word = word.decode('utf8')
        
        if not os.path.exists('./' + word):
            os.mkdir('./' + word)
        # 判断名字是否重复，获取图片长度
        self.__counter = len(os.listdir('./' + word)) + 1
   
        for image_info in rsp_data['imgs']:
            try:
                time.sleep(self.time_sleep)
                # fix = self.__get_suffix(image_info['objURL'])
                # urllib.urlretrieve(image_info['objURL'], './' + word + '/' + str(self.__counter) + str(fix))
                name = self.__get_image_name(image_info['objURL'])
                urllib.urlretrieve(image_info['objURL'], './' + word + '/' + name)
            except urllib2.HTTPError as urllib_err:
                print urllib_err
                continue
            except Exception as err:
                time.sleep(1)
                print err
                print u'产生未知错误，放弃保存'
                continue
            else:
                print u'小黄图+1,已有' + str(self.__counter) + u'张小黄图'
                self.__counter += 1
    
        return

    # 获取后缀名
    @staticmethod
    def __get_suffix(name):
        m = re.search(r'\.[^\.]*$', name)
        
        if m.group(0) and len(m.group(0)) <= 5:
            return m.group(0)
        else:
            return '.jpeg'
        
    # 获取名字
    @staticmethod
    def __get_image_name(name):
        m = re.search(r'\/[^\/]*$', name)
        real_name = m.group(0)[1:len(m.group(0))]
        
        if cmp(real_name[len(real_name) - 4:len(real_name)], '.jpg'):
            return real_name + '.jpg'
        return real_name
    
    # 获取前缀
    @staticmethod
    def __get_prefix(name):
        return name[:name.find('.')]

    # 开始获取
    def __get_images(self, word='美女'):

        search = urllib.quote(word)

        # pn int 图片数
        pn = self.__start_amount
 
        while pn < self.__amount:

            url = "http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word=" + search + "&cg=girl&pn=" + str(
                pn) + "&rn=60&itg=0&z=0&fr=&width=&height=&lm=-1&ic=0&s=0&st=-1&gsm=1e0000001e"
            # 设置header防ban
            try:
                time.sleep(self.time_sleep)
                req = urllib2.Request(url=url, headers=self.headers)
                page = urllib2.urlopen(req)
                rsp = page.read().decode('unicode_escape')
            except UnicodeDecodeError as e:
                print e
                print '-----UnicodeDecodeErrorurl:', url
            except urllib2.URLError as e:
                print e
                print '-----urlErrorurl:', url
            except socket.timeout as e:
                print e
                print '-----socket timout:', url
            else:
                # 解析json
                rsp_data = json.loads(rsp)
                self.__save_image(rsp_data, word)
                # 读取下一页
                print u'下载下一页'
                pn += 60
            finally:
                # page.close()
                pass
        print u'下载任务结束'
        return

    def start(self, word, spider_page_num=1, start_page=1):
        """
        爬虫入口
        :param word: 抓取的关键词
        :param spider_page_num: 需要抓取数据页数 总抓取图片数量为 页数x60
        :param start_page:起始页数
        :return:
        """
        self.__start_amount = (start_page - 1) * 60
        self.__amount = spider_page_num * 60 + self.__start_amount
        self.__get_images(word)
        
def task(name, page_num, start_page):
   crawler = Crawler(0.05)
   crawler.start(name, page_num, start_page)  

if __name__ == "__main__":
    
    threads = []

    t1 = threading.Thread(target=task, args=('百褶裙', 1000, 20,))
    threads.append(t1) 
    t2 = threading.Thread(target=task, args=('领带', 5000, 5,))
    threads.append(t2)

    '''
    t3 = threading.Thread(target=task, args=('反光服', 1000, 20,))
    threads.append(t3) 
    t4 = threading.Thread(target=task, args=('防化服', 1000, 20,))
    threads.append(t4)
    t5 = threading.Thread(target=task, args=('冬季羽绒服', 1000, 1,))
    threads.append(t5)
    t6 = threading.Thread(target=task, args=('卫衣', 1000, 1,))
    threads.append(t6)
    '''
    
    for t in threads:
        t.setDaemon(True)
        t.start()
