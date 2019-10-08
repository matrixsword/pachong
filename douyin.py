# -*- coding:utf-8 -*-
import requests
from contextlib import closing
import os
class DouYin(object):
     def video_downloader(self, video_url, video_name, watermark_flag=True):
        #size = 0
        #chunk_size = 1024 
        req=requests.get(video_url)
        with open(video_name, "wb") as file:  
            #for data in response.iter_content(chunk_size = chunk_size):
            #print(os.path.abspath(video_name))
            file.write(req.content)
            #size += len(data)
            file.flush()
        print('download ok')

