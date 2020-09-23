from selenium.webdriver.common.keys import Keys
from colored import fg, bg, attr
from selenium import webdriver
import urllib.request
import time
import warnings
import os
from PIL import Image

warnings.filterwarnings("ignore", category=DeprecationWarning)

def delay(times):
    times = int(times)
    time.sleep(times)

class Instagram:
    
    def __init__ (self):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_argument("--log-level=3")
        self.browserProfile.add_argument('--hide-scrollbars')
        self.browserProfile.add_experimental_option('excludeSwitches',['enable-logging'])
        self.browserProfile.add_experimental_option('prefs',{"intl.accept_languages":"en,en_US"})

    def showpic(self):
        os.system("cls")
        show = input("\n%sWhat do you want to delete? [post / pp] :%s" % (fg(30), attr(0)))
        if show == "pp":
            try:
                img = Image.open("images/igpp.png")
                img.show() 
            except FileNotFoundError:
                print("\n%s---> There is not screenshot yet%s\n" % (fg(1), attr(0)))
        elif show == "post":
            try:
                img = Image.open("images/igpost.png")
                img.show() 
            except FileNotFoundError:
                print("\n%s---> There is not screenshot yet%s\n" % (fg(1), attr(0)))        

    def deletepic(self):
        os.system("cls")
        delete = input("\n%sWhat do you want to delete? [post / pp / all] :%s" % (fg(30), attr(0)))
        if delete == "pp":
            try:
                os.remove("images/igpp.png")
                print("\n%s---> Deleted!%s\n" % (fg(2), attr(0)))
            except FileNotFoundError:
                print("\n%s---> There is not screenshot yet%s\n" % (fg(2), attr(0)))
        elif delete == "post":
            try:
                os.remove("images/igpost.png")
                print("\n%s---> Deleted!%s\n" % (fg(2), attr(0)))
            except FileNotFoundError:
                print("\n%s---> There is not screenshot yet%s\n" % (fg(2), attr(0)))
        elif delete == "all":
            try:
                os.remove("images/igpp.png")
                print("%s---> Deleted!%s" % (fg(2), attr(0)))
            except FileNotFoundError:
                pass
            
            try:
                os.remove("images/igpost.png")
                print("%s---> Deleted!%s\n" % (fg(2), attr(0)))
            except FileNotFoundError:
                pass

    def profilephoto(self,username):
        self.browserProfile.add_argument("--headless")
        self.browserProfile.add_argument("--disable-gpu")
        self.browser = webdriver.Chrome("driver/chromedriver.exe", chrome_options=self.browserProfile)
        os.system("cls")
        self.username = username
        print("\n%s--> Processing...%s" % (fg(1), attr(0)))
        self.browser.get("http://izuum.com/index.php")
        print("\n%s--> Searching image...\n %s" % (fg(226), attr(0)))
        username = self.browser.find_element_by_xpath("//*[@id='birds']")
        username.send_keys(self.username)
        username.send_keys(Keys.ENTER)
        delay(3)
        byt = self.browser.find_element_by_xpath("//*[@id='et-boc']/div/div[3]/div/div/div/div/center[1]/img")
        src = byt.get_attribute("src")
        urllib.request.urlretrieve(src, "images/igpp.png")
        print("%s--> Downloaded!%s" % (fg(46), attr(0)))
        self.browser.close()

    def postpicture(self,link):
        self.browserProfile.add_argument("--headless")
        self.browserProfile.add_argument("--disable-gpu")
        os.system("cls")
        self.link = link
        print("%s---> Loading...%s" % (fg(2), attr(0)))
        self.browser = webdriver.Chrome("driver/chromedriver.exe", chrome_options=self.browserProfile)
        self.browser.get(link)
        delay(2)
        img = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/div/div/div[1]/div[1]/img')
        src = img.get_attribute("src")
        urllib.request.urlretrieve(src, "images/igpost.png")
        print("%s---> DONE!%s" % (fg(2), attr(0)))
        self.browser.close()

    def freezeAccount(self,username,password):
        self.browserProfile.add_argument("--headless")
        self.browserProfile.add_argument("--disable-gpu")
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome("driver/chromedriver.exe", chrome_options=self.browserProfile)
        self.browser.get("https://www.instagram.com/accounts/login")
        delay(1)
        print("%s\n---> Login in%s\n" % (fg(2), attr(0)))
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(self.username)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(self.password)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
        delay(3)
        print("%s---> Account freezing%s\n" % (fg(2), attr(0)))
        self.browser.get('https://www.instagram.com/accounts/remove/request/temporary/')
        self.browser.find_element_by_xpath('//*[@id="deletion-reason"]').click()
        delay(1)
        self.browser.find_element_by_xpath("//option[@value='need-break']").click()
        self.browser.find_element_by_xpath('//*[@id="password"]').send_keys(self.password)
        delay(2)
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/form/div[3]/button').click()
        delay(2)
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/form/div[4]/div/div[3]/div[1]/button').click()
        print("%s---> Results coming%s\n" % (fg(2), attr(0)))
        delay(1)
        self.browser.save_screenshot("result.png")
        img = Image.open("result.png")
        delay(2)
        img.show()
        self.browser.close()

    def igtv(self):
        self.browser = webdriver.Chrome("driver/chromedriver.exe", chrome_options=self.browserProfile)
        self.browser.get("https://igtools.net/service/igtv")
        print("*"*40)
        input("Press any key when recaptcha done: ")
        link = input("%sIGTV LINK: %s" % (fg(2), attr(0)))
        self.browser.find_element_by_xpath('//*[@id="feed_form"]/div/input').send_keys(link)
        self.browser.find_element_by_xpath('//*[@id="feed_area"]/div[3]/button').click()
        delay(4)
        count = 0
        while True:
            print("%sSENDING...%s" % (fg(2), attr(0)))
            count+=50
            print(f"Total View: %s{count}%s" % (fg(2), attr(0)))
            number = "50"
            self.browser.find_element_by_name('quantity').send_keys(number)
            self.browser.find_element_by_id('submit').click()
            print("%sWAITING FOR 2 MIN..%s" % (fg(1), attr(0)))
            delay(127)

    def video(self):
        self.browser = webdriver.Chrome("driver/chromedriver.exe", chrome_options=self.browserProfile)
        self.browser.get("https://igtools.net/service/views")
        print("*"*40)
        input("Press any key when recaptcha done: ")
        link = input("%sVIDEO LINK: %s" % (fg(2), attr(0)))
        self.browser.find_element_by_xpath('//*[@id="feed_form"]/div/input').send_keys(link)
        self.browser.find_element_by_xpath('//*[@id="feed_area"]/div[3]/button').click()
        delay(4)
        count = 0
        while True:
            print("%sSENDING...%s" % (fg(2), attr(0)))
            count+=50
            print(f"Total View: %s{count}%s" % (fg(2), attr(0)))
            number = "50"
            self.browser.find_element_by_xpath('//*[@id="process_form"]/div[2]/input').send_keys(number)
            self.browser.find_element_by_xpath('//*[@id="submit"]').click()
            print("%sWAITING FOR 2 MIN..%s" % (fg(1), attr(0)))
            delay(127)        

while True:
    print(" ")
    print("%s - - - INSTAGRAM TOOL - - - %s" % (fg(207), attr(0)))
    print(" ")
    secim = input("%s[1]- Download Profile Picture\n[2]- Download Picture Post\n[3]- Freeze Account\n[4]- Send IGTV Viewer\n[5]- Send Video Viewer\n[6]- Show Pictures\n[7]- Delete Pictures\n[8]- Exit\n%s \nEnter Number:" % (fg(207), attr(0)))
    if secim == "1":
        username = input("%susername: %s" % (fg(207), attr(0)))
        Instagram().profilephoto(username)
    elif secim == "8":
        print("%sGOODBYE BABE%s" % (fg(207), attr(0)))
        delay(1)
        exit()
    elif secim == "2":
        link = input("%sPicture Link: %s" % (fg(207), attr(0)))
        Instagram().postpicture(link)
    elif secim == "3":
        username = input("%susername: %s" % (fg(207), attr(0)))
        password = input("%spassword: %s" % (fg(207), attr(0)))
        Instagram().freezeAccount(username,password)
    elif secim == "4":
        Instagram().igtv()
    elif secim == "5":
        Instagram().video()
    elif secim == "6":
        Instagram().showpic()
    elif secim == "7":
        Instagram().deletepic()


# - PAST AD FOR igtool

    # PAST AD
    # self.browser.find_element_by_xpath('/html/body/div/div/div/div/div/div/div/a').click()
    # delay(11)
    # self.browser.find_element_by_xpath('/html/body/main/div/center/div[2]/a').click()
    # delay(2)
    # self.browser.get("https://igtools.net/service/views")