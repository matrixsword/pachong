
import os
import subprocess
import time,pyperclip
from appium import webdriver
import pyautogui
class Action():
    def __init__(self):
        print("**打开kuaishou***")
        #os.system("mitmdump")
        #subprocess.Popen("mitmdump")
        # 初始化配置，设置Desired Capabilities参数
        self.desired_caps ={ 'platformName': 'Android',
                #'platformVersion': '6.0.1',
                'deviceName': 'google_Pixel_2',
                'noReset': True,#不清除登录信息
                'appPackage': 'com.smile.gifmaker',
                'appActivity': 'com.yxcorp.gifshow.HomeActivity',
                'unicodeKeyboard': True,
                'resetKeyboard': True
                #'clearSystemFiles':True
                }
        # 指定Appium Server
        self.server = 'http://localhost:4723/wd/hub'
        # 新建一个Session
        self.driver = webdriver.Remote(self.server, self.desired_caps)
        print("**成功打开kuaishou***")
        self.login()
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
        #sleep(3)
        time.sleep(30)
        # app开启之后点击一次屏幕，确保页面的展示
        #self.driver.tap([(500, 1200)], 500)
        self.driver.tap([(360, 648)], 500)
    def scroll(self):
        # 无限滑动
        while True:
            # 模拟滑动
            #self.driver.swipe(self.start_x, self.start_y,self.end_x,self.end_y)
            # 设置延时等待
            time.sleep(1)
    def search_download(self):
        key = input("请输入要下载视频的关键字：")
       # while key:
        #    key = input("请输入要下载视频的关键字：")
        search = self.driver.find_elements_by_id("com.smile.gifmaker:id/left_btn")
        while len(search) == 0:
            time.sleep(1)
            search = self.driver.find_elements_by_id("com.smile.gifmaker:id/left_btn").set_value()
        search[0].click()

        tab = self.driver.find_elements_by_id("com.smile.gifmaker:id/tab_search")
        while len(tab) == 0:
            time.sleep(1)
            tab = self.driver.find_elements_by_id("com.smile.gifmaker:id/tab_search")
        tab[0].click()

        hint = self.driver.find_elements_by_id("com.smile.gifmaker:id/inside_editor_hint")
        while len(hint) == 0:
            time.sleep(1)
            hint = self.driver.find_elements_by_id("com.smile.gifmaker:id/inside_editor_hint")
        hint[0].click()

        editor =self.driver.find_elements_by_id("com.smile.gifmaker:id/editor")
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
        #editor[0].paste()    没有
        #editor.send_keys(key)没有

        right_tv = self.driver.find_elements_by_id("com.smile.gifmaker:id/right_tv")
        while len(right_tv) == 0:
            time.sleep(1)
            right_tv = self.driver.find_elements_by_id("com.smile.gifmaker:id/right_tv")
        right_tv[0].click()       
        #time.sleep(2)
        # self.driver.tap([(149,710)],500)
        # time.sleep(1)
        # self.driver.tap([(440, 100)],500)
        # time.sleep(2)
        # self.driver.tap([(190, 93)],500)
        # time.sleep(1)
        # self.driver.find_element_by_id("com.smile.gifmaker:id/editor").set_value(key)
        # time.sleep(1)
        # self.driver.tap([(838, 97)],500)

    def main(self):
        #self.comments()
        #self.scroll()
        self.search_download()

if __name__ == '__main__':
    action = Action()
    action.main()

 
# driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)#启动app
# time.sleep(10) #app启动后等待3秒，方便元素加载完成
# # 截图
# print(os.path.abspath(os.path.dirname(__file__)))
# img_folder = os.path.abspath(os.path.dirname(__file__)) + '/screenshots/'
# time =time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
# screen_save_path = img_folder + time + '.png'
# driver.get_screenshot_as_file(screen_save_path)