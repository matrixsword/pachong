from selenium import webdriver
import threading
import printcolor
from selenium.common.exceptions import TimeoutException


chrome_options = webdriver.ChromeOptions()
prefs = {
    'profile.managed_default_content_settings.images': 2,
    'profile.managed_default_content_settings.javascript': 0
}
chrome_options.add_experimental_option('prefs',prefs)
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_argument("--proxy-server=http://127.0.0.1:8889")
chrome_options.add_argument("--window-size=0,0")
clr=printcolor.Color()
class ReqThread(threading.Thread):

    def __init__(self,threadName,mylist):#, keyword,title,url,upname,flag):
        print('inistalizd zzzzzzzzzzzzzzzzzzz')
        super(ReqThread, self).__init__(name=threadName)

        self.__keyword = mylist[0]

        self.__title = mylist[1]

        self.__url = mylist[2]
        self.__upname = mylist[3]
        self.__flag = mylist[4]

 

    def run(self):
        print('cur threa:',threading.current_thread().getName())
        self.driver = webdriver.Chrome(executable_path='D:/chromedriver.exe',chrome_options=chrome_options)
        self.driver.set_page_load_timeout(10)
        try:
            self.driver.get(self.__url)
        except TimeoutException:
            clr.print_red_text('time out after 3 seconds when loading page')
        
