# -*- coding:utf-8 -*-
from splinter.driver.webdriver.chrome import Options, Chrome
from splinter.browser import Browser
from contextlib import closing
import requests, json, time, re, os, sys, time
from bs4 import BeautifulSoup
import conn_mysql
import threading
class Downloader(object):
    def __init__(self, width = 500, height = 300):
        """
        抖音App视频下载
        """
        # 无头浏览器
        chrome_options = Options()
        chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"')
       # self.driver = Browser(driver_name='chrome', executable_path='D:/chromedriver', options=chrome_options, headless=True)


    def video_downloader(self, video_url, video_name, watermark_flag=True):
        """
        视频下载：提供视频地址即可
        Parameters:
            video_url: 带水印的视频地址
            video_name: 视频名
            watermark_flag: 是否下载不带水印的视频
        Returns::14.11655855178833 
            无
        """
        print('in real dowlnad current thread:',threading.current_thread().getName(),'thre nums:',threading.active_count())
        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&:',video_name)
        size = 0
        # if watermark_flag == True:
        #     video_url = self.remove_watermark(video_url)
        # else:
        #     video_url = self.get_download_url(video_url)
        with closing(requests.get(video_url, stream=True, verify = False)) as response:
            chunk_size = 1024
            #content_size = int(response.headers['content-length']) 
            if response.status_code == 200:
                #sys.stdout.write('  [文件大小]:%0.2f MB\n' % (content_size / chunk_size / 1024))
                with open(video_name, "wb") as file: 
                    for data in response.iter_content(chunk_size = chunk_size):
                        file.write(data)
                        size += len(data)
                        file.flush()
        print('下载完一个      视频')
        #time.sleep(0.5)
                        #sys.stdout.write('  [下载进度]:%.2f%%' % float(size / content_size * 100) + '\r')
                        #sys.stdout.flush()


#    def remove_watermark(self, video_url):
#         """
#         获得无水印的视频播放地址
#         Parameters:
#             video_url: 带水印的视频地址
#         Returns:
#             无水印的视频下载地址
#         """
#         self.driver.visit('http://douyin.iiilab.com/')
#         self.driver.find_by_tag('input').fill(video_url)
#         self.driver.find_by_xpath('//button[@class="btn btn-default"]').click()
#         html = self.driver.find_by_xpath('//div[@class="thumbnail"]/div/p')[0].html
#         bf = BeautifulSoup(html, 'lxml')
#         return bf.find('a').get('href')

    def run(self,data_list):
        conn = conn_mysql.Connection()
        ret = conn.search()

        new_data_list = []
        s = set()
        for row in ret:
            s.add(row[2])
       
        for num in range(len(data_list)):
            url = data_list[num][2]
            name = data_list[num][1] 
            if name in s:
                continue
            new_data_list.append(data_list[num])
            video_name="kuaishou"+"/"+name+".mp4"
            self.video_downloader(url,video_name)
        conn.add(new_data_list,"meipai")
        print('下载maipai video完成!')
    #合并下载
    def runDownload(self,folder,data_list):
        conn = conn_mysql.Connection()
        if folder == "haokan":
            ret = conn.searchHaoKan()
        if folder == "haotu":
            ret = conn.searchHaoTu()
        if folder == "yidian":
            ret = conn.searchYiDian()
        if folder == "tiantian":
            ret = conn.searchTianTian()
        if folder == "qutou":
            ret = conn.searchQuTou()
        if folder == "douyin":
            ret = conn.searchDouYin()
        if folder == "souhu":
            ret = conn.searchSouHu()
        if folder == "wangyi":
            ret = conn.searchWangYi()
        if folder == "weibo":
            ret = conn.searchWeiBo()
        
        new_data_list = []
        s = set()
        for row in ret:
            s.add(row[2])

       
        for num in range(len(data_list)):
            url = data_list[num][2]
            name = data_list[num][1].replace('"','').replace("'",'')
            
            if name in s:
                continue
            new_data_list.append(data_list[num])
            video_name=folder+"/"+name+".mp4"
            print('in xunhuan====:',name,url)
            t = threading.Thread(target=self.video_downloader,args=(url,video_name))
            t.start()
        conn.add(new_data_list,folder)
        print('下载',folder,'video 完成!')

    def hello(self):
        """
        打印欢迎界面
        Parameters:
            None
        Returns:
            None
        """
        print('*' * 100)
        print('\t\t\t\t抖音App视频下载小助手')
        print('*' * 100)


if __name__ == '__main__':
    downloader = Downloader()