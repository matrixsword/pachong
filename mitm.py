from mitmproxy import ctx,http
import json
import os,time,re
import downloader,appium
import appiumOp,conn_mysql
import emoji
from urllib.parse import urlencode,  quote, quote_plus, unquote, unquote_plus
import seleniumThread
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import printcolor
from selenium.common.exceptions import TimeoutException
import regularEx,threading,glob,redis
ttian_dict = {}
#index=0
class Download:
    
    def response(self,flow):
        down_loader = downloader.Downloader()
        data_list = []

        #下载个人主页里面视频,flag=1
        if "xxxfeed/profile2?" in flow.request.url and flow.response.status_code == 200:
            print("下载个人主页里面视频")
            html = json.loads(flow.response.text)
            for i in range(len(html["feeds"])):
                if "adaptationSet" in html["feeds"][i]:
                    url = html["feeds"][i]["adaptationSet"][0]["representation"][0]["urls"][0]["url"]                       
                    upname = html["feeds"][i]["user_name"]         
                    title = str(html["feeds"][i]["caption"]).strip()
                    if '\\' in title:
                        title = title.replace('\\', '')
                    if '\n' in title:
                        title = title.replace('\n', '')
                    p = re.compile(r"[?*><:|/]")
                    title = re.sub(p,"",title)                  
                    tur = ("",title,url,upname,1)
                    data_list.append(tur)
            #下载视频            
            down_loader.run(data_list)

        #下载搜索关键字后的视频,flag=2
        if "rest/n/search?" in flow.request.url and flow.response.status_code == 200:
            print("下载搜索关键字后的视频")
            con =flow.request.content.decode()
            keyword = unquote(con[8:con.index('&')])
            print()
            #time.sleep(2)
            html = json.loads(flow.response.text)
            for i in range(len(html["feeds"])):
                if "adaptationSet" in html["feeds"][i]:
                    url = html["feeds"][i]["adaptationSet"][0]["representation"][0]["urls"][0]["url"]    
                    title = str(html["feeds"][i]["caption"]).strip()
                    #title = emoji.demojize(title)
                    if '\\' in title:
                        title = title.replace('\\', '')
                    if '\n' in title:
                        title = title.replace('\n', '')
                    p = re.compile(r"[?*><:|/]")
                    title = re.sub(p,"",title)
                    upname = html["feeds"][i]["user_name"]
                    if '\\' in upname:
                        upname = upname.replace('\\', '')
                    if '\n' in upname:
                        upname = upname.replace('\n', '')
                    p = re.compile(r"[?*><:|/]")
                    upname = re.sub(p,"",upname)               
                    tur = (keyword,title,url,upname,'2')
                    data_list.append(tur)
            #下载视频            
            down_loader.run(data_list)
            
        #下载未登录发现视频,flag=0
        if "xxxfeed/hot" in flow.request.url and flow.response.status_code == 200:
            print("下载未登录发现视频")
            html = json.loads(flow.response.text)
            for i in range(len(html["feeds"])):
                if "adaptationSet" in html["feeds"][i]:
                    url = html["feeds"][i]["adaptationSet"][0]["representation"][0]["urls"][0]["url"]    
                    upname = html["feeds"][i]["user_name"]
                    title = str(html["feeds"][i]["caption"]).strip()
                    if '\\' in title:
                        title = title.replace('\\', '')
                    if '\n' in title:
                        title = title.replace('\n', '')
                    p = re.compile(r"[?*><:|/]")
                    title = re.sub(p,"",title)

                    tur = ("",title,url,upname,0)
                    data_list.append(tur)
            #下载视频            
            down_loader.run(data_list)
        
        #以下是下载好看视频的内容
        ##下载haokan视频
        if "haokan/api?log=" in flow.request.url and flow.response.status_code == 200:
            html = json.loads(flow.response.text)
            videoList = []
            if "feed" in html:
                videoList = html["feed"]["data"]["list"]
            if "search" in html:
                videoList = html["search"]["data"]["list"]

            for i in range(len(videoList)):
                if "feed" in html:
                    title = str(videoList[i]["content"]["title"]).strip()
                    flag = '0'
                    src = videoList[i]["content"]
                if "search" in html:
                    title = str(videoList[i]["title"]).strip()
                    flag = 1
                    keyword = html["search"]["data"]["cate"]
                    src = videoList[i]

                if '\\' in title:
                    title = title.replace('\\', '')
                if '\n' in title:
                    title = title.replace('\n', '')
                p = re.compile(r"[?*><:|/]")
                title = re.sub(p,"",title)
                
                if "feed" in html:
                    keyword = title

                url = src["video_src"]
                upname = src["author"]

                tur = (keyword,title,url,upname,flag)
                data_list.append(tur)
            down_loader.runDownload("haokan",data_list)

class Haotu:
    mylist =[None] * 5
    down_loader = downloader.Downloader()
    def response(self,flow):        
        #video detail:
        if "howtodo.yilan.tv/video/detail" in flow.request.url and flow.response.status_code == 200:
            html = json.loads(flow.response.text)

            self.mylist[1] = html["name"]
            self.mylist[3] = html["cp_info"]["cp_name"]
            self.mylist[0] = html["category"]
            self.mylist[4] = 0
            #mylist is full,notnone
            if self.mylist[2]:
                #download,clear
                #print("in deatil: send",self.mylist,list(tuple(self.mylist)))
                self.down_loader.runDownload("haotu",[tuple(self.mylist)])
                self.mylist =[None] * 5
        if "howtodo.yilan.tv/video/play" in flow.request.url and flow.response.status_code == 200:
            html = json.loads(flow.response.text)

            self.mylist[2] = html["bitrates"][0]["uri"]
            #mylist is full
            if self.mylist[0]:
                #download,clear
                #print("in play :send",self.mylist,list(tuple(self.mylist)))
                self.down_loader.runDownload("haotu",[tuple(self.mylist)])
                self.mylist =[None] * 5
class Qutou:
    down_loader = downloader.Downloader()
    def response(self,flow):
        #main-profile video
        if 'wemedia/content/all' in flow.request.url and flow.response.status_code == 200:
            print("*******************in main:")
            html = json.loads(flow.response.text)
            data_list = []
            sour = html["data"]["list"]
            num = len(sour)
            for i in range(num):
                keyword = ','.join(sour[i]["content"]["tag"])
                upname = sour[i]["content"]["nickname"]
                if 'hd' in sour[i]["content"]["video_info"]:
                    url = sour[i]["content"]["video_info"]["hd"]["url"]
                else:
                    url = sour[i]["content"]["video_info"]["ld"]["url"]
                title = sour[i]["content"]["title"]
                flag = 0
                tur = (keyword,title,url,upname,flag)
                data_list.append(tur)
            self.down_loader.runDownload("qutou",data_list)

        #search-download
        if 'search/searchContentNew?' in flow.request.url and flow.response.status_code == 200:
            print("*******************in serch:")
            html = json.loads(flow.response.text)
            data_list = []
            sour = html["data"]["news"]["card"]
            num = len(sour)
            for i in range(num):
                keyword = ','.join(sour[i]["tag"])
                upname = sour[i]["nickname"]
                if 'hd' in sour[i]["video_info"]:
                    url = sour[i]["video_info"]["hd"]["url"]
                else:
                    url = sour[i]["video_info"]["ld"]["url"]
                title = sour[i]["title"]
                flag = 1
                tur = (keyword,title,url,upname,flag)
                data_list.append(tur)
            self.down_loader.runDownload("qutou",data_list)
class Douyin:
    pool = redis.ConnectionPool(host='localhost', port=6379,db=1)
    red = redis.Redis(connection_pool=pool)
    down_loader = downloader.Downloader()
    def response(self,flow):
        #main-profile video
        if 'aweme/v1/aweme/post' in flow.request.url and flow.response.status_code == 200:
            print("$$$$$$$$$$$$$$ in main $$$$$$$$$$$$$$$$$$$")
            html = json.loads(flow.response.text)
            data_list = []
            sour = html["data"]
            num = len(sour)
            for i in range(num):
                if not 'aweme_info' in sour[i]:
                    continue
                keyword = sour[i]['author']["signature"]
                upname = sour[i]["author"]["nickname"]
                url = sour[i]['video']['bit_rate'][0]['play_addr']['url_list'][0]
                title = sour[i]["desc"]
                flag = 1
                tur = (keyword,title,url,upname,flag)
                data_list.append(tur)
            self.down_loader.runDownload("douyin",data_list)
        
        #search video
        if 'aweme/v1/general/search/single' in flow.request.url and flow.response.status_code == 200:
            print("%%%%%%%%%%%%%%in search%%%%%%%%%%%%%%")
            #keyword = flow.request.keyword//meiyou,content:keyword=b&...
            con =flow.request.content.decode()
            keyword = unquote(con[8:con.index('&')])
            #keyword = con.replace('%','\\x').encode()          
            html = json.loads(flow.response.text)
            data_list = []
            sour = html["data"]
            num = len(sour)
            for i in range(num):
                #过滤掉user_list
                if not "aweme_info" in sour[i]:
                    continue
                upname = sour[i]["aweme_info"]["author"]["nickname"]
                url = sour[i]["aweme_info"]['video']['bit_rate'][0]['play_addr']['url_list'][0]
                title = sour[i]["aweme_info"]["desc"]
                flag = 2
                tur = (keyword,title,url,upname,flag)
                data_list.append(tur)
            self.down_loader.runDownload("douyin",data_list)
        #shouyedouyin video
        #target_urls = ['v6-dy.ixigua.com','v6-dy.ixigua.com','v9-dy.ixigua.com','v27-dy.ixigua.com']
        data_list = []
        if 'ixigua.com' in flow.request.url:
            flag = self.red.sadd('douyin_test',flow.request.url)
            if flag:
                tur = ('unkeyd','test{}'.format(self.red.scard('douyin_test')),flow.request.url,'unnamed',0)
                data_list.append(tur)
                self.down_loader.runDownload("douyin",data_list)
            

class Yidian:
    down_loader = downloader.Downloader()
    def response(self,flow):
        #main-profile video
        if 'xxxaweme/v1/aweme/post' in flow.request.url and flow.response.status_code == 200:
            print("$$$$$$$$$$$$$$ in main $$$$$$$$$$$$$$$$$$$")
            html = json.loads(flow.response.text)
            data_list = []
            sour = html["data"]
            num = len(sour)
            for i in range(num):
                if not 'aweme_info' in sour[i]:
                    continue
                keyword = sour[i]['author']["signature"]
                upname = sour[i]["author"]["nickname"]
                url = sour[i]['video']['bit_rate'][0]['play_addr']['url_list'][0]
                title = sour[i]["desc"]
                flag = 1
                tur = (keyword,title,url,upname,flag)
                data_list.append(tur)
            self.down_loader.runDownload("douyin",data_list)

class Tiantian:
    global ttian_dict
    mylist = [None] * 5
    down_loader = downloader.Downloader()
    def response(self,flow):
        #print('GGGGGGGGGGGGGGG:CCCCCCCCC::',flow.request.url)
        #main-profile video

        if 'r.cnews.qq.com/getVideoNewsIndex' in flow.request.url and flow.response.status_code == 200:
            print("$$$$$$$$$$$$$$ in down new$$$$$$$$$$$$$$$$$$$")
            html = json.loads(flow.response.text)
            data_list = []
            sour = html["newslist"]
            num = len(sour)
            i=0
            #for i in range(num):
            print('***************list:',i)
            self.mylist[0] = sour[i]['abstract']
            self.mylist[3] = sour[i]["chlname"]
            self.mylist[1] = sour[i]["title"]
            self.mylist[4] = 1
            url = sour[i]['video_channel']['video']['playurl']
            self.mylist[2] = url
            print('**********',url)
            #tur = (keyword,title,url,upname,flag)
            try:
                req=seleniumThread.ReqThread(url,self.mylist)
                req.start()              
            except TimeoutException:  
                print ('time out after 30 seconds when loading page')
            clr=printcolor.Color()
            clr.print_red_text('geturl ok!curtime is : '+str(i)+time.ctime()) 

        #real video url
        if 'om.tc.qq.com' in flow.request.url:
            clr=printcolor.Color()
            clr.print_green_text('&&&&&&&&&&&&&real url，，threa is :'+threading.current_thread().getName()+flow.request.url)
            #ttian_dict[]
            #self.mylist[2] = flow.request.url
            #self.down_loader.runDownload("tiantian",[tuple(self.mylist)])   
        return
class SouHu:
    mylist =[]
    down_loader = downloader.Downloader()
    def response(self,flow):
        #some one video play
        if 'sohu.com/v4/video/detail/' in flow.request.url and flow.response.status_code==200:
            html = json.loads(flow.response.text)
            sour = html["data"]['videoVO']
            keyword=sour['keyword']
            title=sour['video_name']
            url=sour['video_high_mp4']
            upname=sour['user']['nickname']
            flag=0
            tur = (keyword,title,url,upname,flag)
            downloader.Downloader().runDownload('souhu',[tur])
        #main-file video a
        if 'user/home/feedv2' in flow.request.url and flow.response.status_code==200:
            html = json.loads(flow.response.text)
            print('main-file video a')
            data_list = [None]*5
            sour = html["data"]['feeds']
            num = len(sour)
            for i in range(num):
                print("***************",i)
                data_list[1] = sour[i]['content']['content_video']['video_name']
                data_list[3] = data_list[1]#sour[i]['userInfo']['nickname']
                data_list[0] = sour[i]['content']['content_video']['video_name']
                data_list[4] = 1
                self.mylist.append(data_list)
        #main-file video A      
        if "video/plays.do" in flow.request.url and flow.response.status_code == 200:
            urlList = list(json.loads(flow.response.text))
            print('mylist len:%d' %len(self.mylist))
            print('urllist len:%d' %len(urlList))
            for i in range(len(urlList)):
                print('&&&&&&&&&&&&&&&&&&&&&&&&',i)
                url = urlList[i]['playinfo'][0]['downloadUrl']
                self.mylist[i][2] = url
                self.mylist[i] = tuple(self.mylist[i])
            self.down_loader.runDownload('souhu',self.mylist)
            self.mylist = []
        #if 'sohu.com/search/new/keyword' in 

class WangYi:
    down_loader = downloader.Downloader()
    def response(self,flow):
        data_list = []
        if 'recommend/getChanListNews' in flow.request.url and flow.response.status_code == 200:
            clr=printcolor.Color()
            clr.print_blue_text('in wangyi')
            stime=time.time()
            html = json.loads(flow.response.text)
            sour = html['视频']
            num = len(sour)
            for i in range(num):
                clr.print_green_text('**************************'+str(i))
                if 'category' in sour[i]:
                    keyword = sour[i]['category']
                else:
                    keyword = sour[i]['videoTopic']['alias']
                title = sour[i]['title']
                url = sour[i]['mp4_url']
                upname = sour[i]['videoTopic']['tname']
                flag = 0
                tur = (keyword ,title ,url , upname ,flag)
                data_list.append(tur)
            self.down_loader.runDownload('wangyi',data_list)
            etime=time.time()
            print('before down? time :'+str(etime-stime))
            
            

class WeiBo:
    pool = redis.ConnectionPool(host='localhost', port=6379,db=1)
    red = redis.Redis(connection_pool=pool)
    down_loader = downloader.Downloader()
    def response(self,flow):
        data_list = []
        if 'weibo.cn//2/video/tab' in flow.request.url and flow.response.status_code == 200:
            clr=printcolor.Color()
            clr.print_blue_text('in weibo')
            html = json.loads(flow.response.text)
            sour = html['cards']
            num = len(sour)
            for i in range(num):
                keyword = sour[i]['desc']
                title = sour[i]['playlist']['statuses']['page_info']['media_info']['next_title']
                url = sour[i]['playlist']['statuses']['page_info']['media_info']['mp4_hd_url']
                upname = sour[i]['playlist']['name']
                flag = 0
                tur = (keyword , title , url , upname , flag)
                data_list.append(tur)
            self.down_loader.runDownload('weibo',data_list)
            print('before down? time :')
        #second format
        #if 'weibo.cn/2/guest/cardlist' in flow.request.flow and flow.response.status_code == 200:
        if 'weibo.cn/2/searchall' in flow.request.url and flow.response.status_code == 200:
            print('in weiiiiiiiiiiiiiiiiibo')
            html = flow.response.text
            urlList = regularEx.MyRegex().myFindall(html)
            for i in range(len(urlList)):
                url = urlList[i].replace('\\','')
                if url != '':
                    t=threading.Thread(target=self.down_loader.video_downloader,args=(url,'weibo/video{}.mp4'.format(self.red.scard('GTX'))))
                    self.red.sadd('GTX',url)
                    t.start()
            
class Test:
    def response(self,flow):
        print('*****8889*****')
        if 'om.tc.qq.com' in flow.request.url:
            print('********in real url******')
            time.sleep(2)
            


addons = [
    Download(),Haotu(),Qutou(),Douyin(),Yidian(),Tiantian(),WangYi(),WeiBo()
]