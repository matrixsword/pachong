import os
import subprocess
import time,pyperclip
from appium import webdriver
import pyautogui
class Action():
    def __init__(self):
        print("**打开haotu***")
        #os.system("mitmdump")
        #subprocess.Popen("mitmdump")
        # 初始化配置，设置Desired Capabilities参数
        self.desired_caps ={ 'platformName': 'Android',
                #'platformVersion': '6.0.1',
                'deviceName': 'google_Pixel_2',
                'noReset': True,#不清除登录信息
                'appPackage': 'tv.yilan.howto.app',
                'appActivity': 'com.yilan.tech.app.activity.MainActivity',
                'unicodeKeyboard': True,
                'resetKeyboard': True
                #'clearSystemFiles':True
                }
        # 指定Appium Server
        self.server = 'http://localhost:4723/wd/hub'
        # 新建一个Session
        self.driver = webdriver.Remote(self.server, self.desired_caps)
        print("**成功打开haotu***")
        #self.login()
        #time.sleep(10)

    def login(self):
        print("**登录账户***")
        logon = self.driver.find_elements_by_id("com.smile.gifmaker:id/left_text")
        
        if len(logon) > 0:
            print("未登录，现在登录")
            self.driver.find_element_by_id("com.smile.gifmaker:id/left_text").click()
            self.driver.find_element_by_id("com.smile.gifmaker:id/other_login_view").click()

         #self.driver.find_element_by_id("com.smile.gifmaker:id/login_name_et").clear()
            self.driver.find_element_by_id("com.smile.gifmaker:id/login_name_et").set_value("17826519963")
            self.driver.find_element_by_id("com.smile.gifmaker:id/next_view").click()
            time.sleep(3)
        #self.driver.find_element_by_id("com.smile.gifmaker:id/login_psd_et").clear()
            passwd = self.driver.find_element_by_id("com.smile.gifmaker:id/login_psd_et")
            while not passwd:
                time.sleep(1)
                passwd = self.driver.find_element_by_id("com.smile.gifmaker:id/login_psd_et")
            passwd.set_value("kuaishou")
            self.driver.find_element_by_id("com.smile.gifmaker:id/login_view").click()
            time.sleep(2)
            print("登录成功")
        else:
            print("账户已经处于登录状态")
    def comments(self):
 
        time.sleep(30)
 
        self.driver.tap([(360, 648)], 500)
    def scroll(self):
        # 无限滑动
        while True:
            # 模拟滑动
            #self.driver.swipe(self.start_x, self.start_y,self.end_x,self.end_y)
            # 设置延时等待
            time.sleep(1)
    def search_download(self):
        key = input("haotu,请输入要下载视频的关键字：")

        search = self.driver.find_elements_by_id("tv.yilan.howto.app:id/icon_search")
        while len(search) == 0:
            time.sleep(1)
            search = self.driver.find_elements_by_id("com.smile.gifmaker:id/left_btn").set_value()
        search[0].click()

        editor =self.driver.find_elements_by_id("tv.yilan.howto.app:id/icon_search")
        while len(editor) == 0:
            time.sleep(1)
            editor = self.driver.find_elements_by_id("com.smile.gifmaker:id/editor")
        pyperclip.copy(key) 
        editor[0].click()   
        pyautogui.hotkey('ctrl','v')
        time.sleep(1)
        search = editor[0].text
        while search != key:
            time.sleep(1)
            editor[0].clear()
            editor[0].click() 
            pyautogui.hotkey('ctrl','v')
            search = editor[0].text

        right_tv = self.driver.find_elements_by_id("com.smile.gifmaker:id/right_tv")
        while len(right_tv) == 0:
            time.sleep(1)
            right_tv = self.driver.find_elements_by_id("com.smile.gifmaker:id/right_tv")
        right_tv[0].click()       
      

    def main(self):
        #self.comments()
        #self.scroll()
        self.search_download()

if __name__ == '__main__':
    action = Action()
    action.main()

