from selenium.webdriver.common.keys import Keys
from colored import fg, bg, attr
from selenium import webdriver
import urllib.request
import time
import sys
import warnings
import os

warnings.filterwarnings("ignore", category=DeprecationWarning)

#-----------------------------------------------------------------------------------------------------#

class InstaImg:
    
    def __init__ (self):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_argument("--headless")
        self.browserProfile.add_argument("--disable-gpu")
        self.browserProfile.add_argument("--log-level=3")
        self.browserProfile.add_experimental_option('excludeSwitches',['enable-logging'])
        self.browser = webdriver.Chrome("driver/chromedriver.exe", chrome_options=self.browserProfile)

    def Download(self,username):
        self.username = username
        os.system("cls")
        print("%sProcessing...%s" % (fg(1), attr(0)))
        self.browser.get("http://izuum.com/index.php")
        print("%sSearching image...\n %s" % (fg(226), attr(0)))
        username = self.browser.find_element_by_xpath("//*[@id='birds']")
        username.send_keys(self.username)
        username.send_keys(Keys.ENTER)
        time.sleep(3)
        byt = self.browser.find_element_by_xpath("//*[@id='et-boc']/div/div[3]/div/div/div/div/center[1]/img")
        src = byt.get_attribute("src")
        urllib.request.urlretrieve(src, "images/igpp.png")
        print("%sDownloaded!%s" % (fg(46), attr(0)))
        self.browser.close()

    def delete(self):
        os.system("cls")
        try:
            os.remove("images/igpp.png")
            print("\n%s---> Deleted!%s\n" % (fg(2), attr(0)))
        except FileNotFoundError:
            print("\n%s---> There is not screenshot yet%s\n" % (fg(2), attr(0)))

#-----------------------------------------------------------------------------------------------------#

while True:
    print(" ")
    print("%s - - - IG PP DOWNLOADER - - - %s" % (fg(83), attr(0)))
    print(" ")
    secim = input("%s[1]- Search User\n[2]- Delete Pic\n[3]- Exit\n%s \nEnter Number:" % (fg(71), attr(0)))
    if secim == "1":
        username = input("%susername: %s" % (fg(128), attr(0)))
        InstaImg().Download(username)
    elif secim == "3":
        print("%sGOODBYE BABE%s" % (fg(1), attr(0)))
        sys.exit()
    elif secim == "2":
        InstaImg().delete()

#-----------------------------------------------------------------------------------------------------#
