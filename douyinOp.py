import os
import subprocess
import time,pyperclip
from appium import webdriver
import pyautogui
class Action():
    def __init__(self):
        print("**打开douyin***")
        #os.system("mitmdump")
        #subprocess.Popen("mitmdump")
        # 初始化配置，设置Desired Capabilities参数
        self.desired_caps ={ 'platformName': 'Android',
                #'platformVersion': '6.0.1',
                'deviceName': 'google_Pixel_2',
                'noReset': True,#不清除登录信息
                'appPackage': 'com.ss.android.ugc.aweme',
                'appActivity': '.account.login.ui.LoginOrRegisterActivity',
                'unicodeKeyboard': True,
                'resetKeyboard': True
                #'clearSystemFiles':True
                }
        # 指定Appium Server
        self.server = 'http://localhost:4723/wd/hub'
        # 新建一个Session
        self.driver = webdriver.Remote(self.server, self.desired_caps)
        print("**成功打开douyin***")
        self.login()
        #time.sleep(10)

    def login(self):
        a = input("是否登录账户?yes: 1")
        if a == '1':
            print("**登录账户***")
            self.driver.tap([(807,1544)],500)
            user = '17826519963'
            passwd = 'douyin123'
            passwdLogin = self.driver.find_elements_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView")
            while len(passwdLogin) == 0:
                time.sleep(1)
                passwdLogin = self.driver.find_elements_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TextView")
            passwdLogin[0].click()
            #input ui
            userEdit = self.driver.find_elements_by_id("com.ss.android.ugc.aweme:id/a9y")
            while len(userEdit) == 0:
                time.sleep(1)
                userEdit = self.driver.find_elements_by_id("com.ss.android.ugc.aweme:id/a9y")
            userEdit[0].claer()
            userEdit[0].set_value(user)
            while userEdit[0].text != user:
                userEdit[0].claer()
                userEdit[0].set_value(user)
            
            passEdit = self.driver.find_elements_by_id("com.ss.android.ugc.aweme:id/a9x")
            passEdit = self.driver.find_elements_by_id("com.ss.android.ugc.aweme:id/a9x")
            while len(passEdit) == 0:
                time.sleep(1)
                passEdit = self.driver.find_elements_by_id("com.ss.android.ugc.aweme:id/a9x")
            passEdit[0].claer()
            passEdit[0].set_value(passwd)
            while passEdit[0].text != passwd:
                passEdit[0].claer()
                passEdit[0].set_value(passwd)
            
            readBtn = self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/c8o")
            readBtn.click()
            while '未' in readBtn.content-desc:
                time.sleep(1)
                readBtn.click()
            
            loginBtn = self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/os")
            loginBtn.click()
            print("登录成功")


    def comments(self):
 
        time.sleep(30)
 
        self.driver.tap([(360, 648)], 500)
    def scroll(self):
        # 无限滑动
        while True:
            # 模拟滑动
            #self.driver.swipe(self.start_x, self.start_y,self.end_x,self.end_y)
            self.driver.swipe(200, 750,200,200)
            # 设置延时等待
            time.sleep(1)
    def search_download(self):
        key = input("douyin,请输入要下载视频的关键字：")
        self.driver.tap([(833,97)],500)

        search = self.driver.find_elements_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.View/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.view.View")
        search[0].click()
        pyautogui.hotkey('ctrl','v')
        while search[0].text != key:
            search[0].click()
            pyautogui.hotkey('ctrl','v')
        searchBtn = self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/dq8")
        searchBtn.click()

        time.sleep(2)
        self.scroll()
       
      

    def main(self):
        a = input("是否要搜索视频？'yes: 1:'")
        if a == '1':
            self.search_download()
        else:
            self.driver.tap([(300,850)],500)
            time.sleep(2)
            self.scroll()

if __name__ == '__main__':
    action = Action()
    action.main()

