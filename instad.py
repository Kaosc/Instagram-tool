from selenium.webdriver.common.keys import Keys
from colored import fg, bg, attr
from selenium import webdriver
import urllib.request
import time
import sys

#-----------------------------------------------------------------------------------------------------#

class InstaImg:
    
    def __init__ (self):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('excludeSwitches',['enable-logging'])
        self.browserProfile.add_argument("--headless")
        self.browserProfile.add_argument("--disable-gpu")
        self.browserProfile.add_argument("--log-level=3")
        self.browser = webdriver.Chrome("chromedriver.exe", chrome_options=self.browserProfile)
        self.username = username

    def Download(self,username):
        print("%sProcessing...%s" % (fg(1), attr(0)))
        self.browser.get("http://izuum.com/index.php")
        print("%sSearching image...\n %s" % (fg(226), attr(0)))
        username = self.browser.find_element_by_xpath("//*[@id='birds']")
        username.send_keys(self.username)
        username.send_keys(Keys.ENTER)
        time.sleep(3)
        byt = self.browser.find_element_by_xpath("//*[@id='et-boc']/div/div[3]/div/div/div/div/center[1]/img")
        src = byt.get_attribute("src")
        urllib.request.urlretrieve(src, "picture.png")
        print("%sDownloaded!%s" % (fg(46), attr(0)))
        self.browser.close()

#-----------------------------------------------------------------------------------------------------#

while True:
    print(" ")
    print("%s - - - - INSTAGRAM FULL SIZE PP DOWNLOADER - - - - %s" % (fg(83), attr(0)))
    print(" ")
    secim = input("%s[1]- Search User\n[2]- Exit\n[3]- Contact With Me%s\n \nEnter Number:" % (fg(71), attr(0)))
    if secim == "1":
        username = input("%susername: %s" % (fg(128), attr(0)))
        InstaImg().Download(username)
    elif secim == "2":
        print("%sGOODBYE BABE%s" % (fg(1), attr(0)))
        time.sleep(2)
        sys.exit()
    elif secim == "3":
        print(" ")
        print("%sMail Me: kaosc.mail@gmail.com%s" % (fg(75), attr(0)))

#-----------------------------------------------------------------------------------------------------#

# By Kaosc
