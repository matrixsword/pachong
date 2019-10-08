
import requests
import bs4
from multiprocessing.dummy import Pool as ThreadPool
import traceback
from lxml import etree
 
headers = {
    "referer": "https://movie.douban.com/",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",  # 自己使用的浏览器
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/jpg,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch"
}
img_list = []
 
 
def getHTmLText(url):
    try:
        r = requests.get(url, timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("Error!")
 
 
def find_src(html):
    soup = bs4.BeautifulSoup(html, "lxml")
    for i in soup.find_all(class_="cover"):
        for j in i.find_all("img"):
            img_list.append(j["src"])

def find_src2(html):
    mytree = etree.HTML(html)
    urls = mytree.xpath("//div[@class='cover']/a/img/@src")
    img_list.extend(urls)
    #print(mytree)<Element html at 0x1589775dfc8>
 
 
def download_pic(i):
    try:
        content = requests.get(i, headers=headers)
        url_content = content.content
        file_name = "D:/Photos/test/" + i.split("/")[-1][1:]
        f = open(file_name, "wb")
        f.write(url_content)
        f.close()
    except Exception:
        print(traceback.format_exc())
 
 
def main():
    start_url = 'https://movie.douban.com/celebrity/1050453/photos/'
    for i in range(66):
        url = start_url + "?type=C&start=" + str(30 * i)
        html = getHTmLText(url)
        find_src2(html)
    print("done")
 
 
main()
thread_num = 50
pool = ThreadPool(thread_num)
pool.map(download_pic, img_list)
pool.close()
pool.join()