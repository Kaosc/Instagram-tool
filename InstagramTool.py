from selenium.webdriver.common.keys import Keys
from colored import fg, attr
from selenium import webdriver
import urllib.request
import time
import warnings
import os
from PIL import Image

warnings.filterwarnings("ignore", category=DeprecationWarning)

class Instagram:
    
    def __init__ (self):
        self.drvPath = "E:/Code/Git/InstagramBots/driver/chromedriver.exe"              # PATH IS HERE <------------- !
        self.imgPath = "E:/Code/Git/InstagramBots/images"                               # PATH IS HERE <------------- !
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_argument("--lang=en")
        self.browserProfile.add_argument("--log-level=3")
        self.browserProfile.add_argument('--hide-scrollbars')
        # self.browserProfile.add_argument("--headless")    # ---> some methods does not work properly with headless - so it's optional
        self.browserProfile.add_argument("--disable-gpu")
        self.browserProfile.add_experimental_option('excludeSwitches',['enable-logging'])
        self.browserProfile.add_experimental_option('prefs',{"intl.accept_languages":"en,en_US"})

    def login(self,username,password):
        os.system('cls')
        self.browser = webdriver.Chrome(self.drvPath, chrome_options=self.browserProfile)
        print("%s--> Login in\n%s" % (fg(61), attr(0)))
        self.username = username
        self.password = password
        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(self.username)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(self.password)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
        time.sleep(3)    

    def showpic(self):
        os.system("cls")
        show = input("\n%s[post / pp / result] :%s" % (fg(30), attr(0)))
        if show == "pp":
            try:
                img = Image.open(F"{self.imgPath}/igpp.png")
                img.show() 
            except FileNotFoundError:
                print("\n%s---> There is not screenshot yet%s\n" % (fg(1), attr(0)))
        elif show == "post":
            try:
                img = Image.open(F"{self.imgPath}/igpost.png")
                img.show() 
            except FileNotFoundError:
                print("\n%s---> There is not screenshot yet%s\n" % (fg(1), attr(0)))     
        elif show == "result":
            try:
                img = Image.open(F"{self.imgPath}/result.png")
                img.show() 
            except FileNotFoundError:
                print("\n%s---> There is not screenshot yet%s\n" % (fg(1), attr(0)))               

    def deletepic(self):
        os.system("cls")
        delete = input("\n%s[post / pp / result / all] :%s" % (fg(30), attr(0)))
        if delete == "pp":
            try:
                os.remove(f"{self.imgPath}/igpp.png")
                print("\n%s---> Deleted!%s\n" % (fg(2), attr(0)))
            except FileNotFoundError:
                print("\n%s---> There is not screenshot yet%s\n" % (fg(2), attr(0)))
        elif delete == "post":
            try:
                os.remove(f"{self.imgPath}/igpost.png")
                print("\n%s---> Deleted!%s\n" % (fg(2), attr(0)))
            except FileNotFoundError:
                print("\n%s---> There is not screenshot yet%s\n" % (fg(2), attr(0)))
        elif delete == "result":
            try:
                os.remove(f"{self.imgPath}/igpost.png")
                print("\n%s---> Deleted!%s\n" % (fg(2), attr(0)))
            except FileNotFoundError:
                print("\n%s---> There is not screenshot yet%s\n" % (fg(2), attr(0)))
        elif delete == "all":
            try:
                os.remove(f"{self.imgPath}/igpp.png")
                print("%s---> Deleted!%s" % (fg(2), attr(0)))
            except FileNotFoundError:
                pass
            
            try:
                os.remove(f"{self.imgPath}/igpost.png")
                print("%s---> Deleted!%s\n" % (fg(2), attr(0)))
            except FileNotFoundError:
                pass

            try:
                os.remove(f"{self.imgPath}/result.png")
                print("%s---> Deleted!%s\n" % (fg(2), attr(0)))
            except FileNotFoundError:
                pass

    def profilephoto(self,username):
        self.browser = webdriver.Chrome(self.drvPath, chrome_options=self.browserProfile)
        os.system("cls")
        self.username = username
        print("\n%s--> Processing...%s" % (fg(1), attr(0)))
        self.browser.get(f"https://instabig.net/fullsize/{self.username}")
        print("\n%s--> Searching image...\n %s" % (fg(226), attr(0)))
        time.sleep(2)
        byt = self.browser.find_element_by_xpath('//*[@id="imgBigPP"]')
        src = byt.get_attribute("src")
        urllib.request.urlretrieve(src, f"{self.imgPath}/igpp.png")
        print("%s--> Downloaded!%s" % (fg(46), attr(0)))
        self.browser.close()

    def downloadPost(self,link):
        os.system("cls")
        self.link = link
        print("%s---> Loading...%s" % (fg(2), attr(0)))
        self.browser = webdriver.Chrome(self.drvPath, chrome_options=self.browserProfile)
        self.browser.get(link)
        time.sleep(2)
        loc = self.browser.find_elements_by_tag_name("img")[1]
        img = loc.find_element_by_xpath("//div/img")
        src = img.get_attribute('src')
        urllib.request.urlretrieve(src, f"{self.imgPath}/igpost.png")
        print("%s---> DONE!%s" % (fg(2), attr(0)))
        self.browser.close()

    def freezeAccount(self,password):
        os.system("cls")
        self.password = password
        print("%s---> Account freezing%s\n" % (fg(2), attr(0)))
        self.browser.get('https://www.instagram.com/accounts/remove/request/temporary/')
        self.browser.find_element_by_xpath('//*[@id="deletion-reason"]').click()
        time.sleep(2)
        self.browser.find_element_by_xpath("//option[@value='need-break']").click()
        self.browser.find_element_by_xpath('//*[@id="password"]').send_keys(self.password)
        time.sleep(2)
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/form/div[3]/button').click()
        time.sleep(2)
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/form/div[4]/div/div[3]/div[1]/button').click()
        print("%s---> Results coming%s\n" % (fg(2), attr(0)))
        time.sleep(2)
        self.browser.save_screenshot(f"{self.imgPath}/result.png")
        img = Image.open(f"{self.imgPath}/result.png")
        time.sleep(2)
        img.show()
        self.browser.close()

    def navigateFollowers(self,user):
        print("%s--> Navigating\n%s" % (fg(61), attr(0)))
        self.user = user
        self.browser.get(f'https://www.instagram.com/{self.user}')
        time.sleep(1)
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
        time.sleep(2)

    def navigateFollowings(self,user):
        print("%s--> Navigating\n%s" % (fg(61), attr(0)))
        self.user = user
        self.browser.get(f'https://www.instagram.com/{self.user}')
        time.sleep(1)
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()
        time.sleep(2)

    def getUserList(self,total):
        self.total = total
        dialog = self.browser.find_element_by_css_selector("div[role=dialog] ul")
        action = webdriver.ActionChains(self.browser)

        while True:
            dialog.click()
            action.key_down(Keys.PAGE_DOWN).perform()
            time.sleep(0.5)

            newCount = len(dialog.find_elements_by_css_selector("li"))
            print(F"%sTotal Collected: {newCount}%s" % (fg(10), attr(0)))
            
            if newCount <= 1:
                break

            if newCount < total:
                time.sleep(0.5)
            else:
                break

        followers = dialog.find_elements_by_css_selector("li")
        self.mainList = []

        i = 0
        for user in followers:
            link = user.find_element_by_css_selector("a").get_attribute("href")
            self.mainList.append(link)
            i +=1
            if i >= total:
                break

    def follow(self):
        print("%s-->Processing... Get relief until it end.%s" % (fg(45), attr(0)))
        for user in self.mainList:
            self.browser.get(user)
            time.sleep(2)
            self.browser.find_element_by_xpath('//button[text()="Follow"]').click()
            time.sleep(1)

    def unFollow(self):
        print("%s--> Processing... Get relief until it end.%s" % (fg(45), attr(0)))
        for user in self.mainList:
            self.browser.get(user)
            time.sleep(2)
            self.browser.find_element_by_css_selector("[aria-label='Following']").click()
            time.sleep(0.5)
            self.browser.find_element_by_css_selector("div[role=dialog]").click()
            self.browser.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[1]').click()
            time.sleep(1)

    def message(self):
        print("%s\n--> DONE%s" % (fg(1), attr(0)))

    def closeBot(self):
        self.browser.close()

    def getFollowers(self,username):
        os.system('cls')
        self.username = username
        self.browser.get(f"https://www.instagram.com/{self.username}")
        time.sleep(2)
    
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
        print("%sCounting Followers%s" % (fg(2), attr(0)))

        time.sleep(2)
    
        actionBox = self.browser.find_element_by_css_selector("div[role=dialog] ul")
        CurrentFollowers = len(self.browser.find_elements_by_css_selector('li'))
        print(f"First Time Counting Followers: {CurrentFollowers}")
    
        action = webdriver.ActionChains(self.browser)

        while True:
            actionBox.click()
            action.key_down(Keys.PAGE_DOWN).key_down(Keys.PAGE_DOWN).key_down(Keys.PAGE_DOWN).perform()
            time.sleep(1)
    
            newCount = len(self.browser.find_elements_by_css_selector('li'))
    
            if CurrentFollowers != newCount:
                CurrentFollowers = newCount
                print(f"Collected Followers: {newCount}")
                time.sleep(1)
            else:
                break
            
        totalFollowers = actionBox.find_elements_by_css_selector('li')
    
        Flist = []
        i = 0
        for users in totalFollowers:
            i += 1
            if i == CurrentFollowers:
                break
            
            time.sleep(0.5)
            link = users.find_element_by_css_selector("a").get_attribute("href")
            Flist.append(link)

        print("Saving...")

        with open("followers.txt","w",encoding="utf-8") as file:
            for item in Flist:
                file.write(item+ "\n")

        print("%sDone!\nAll Followers Saved to 'followers.txt' file. %s" % (fg(2), attr(0)))

        self.browser.close()

Instagram = Instagram()

while True:
    print("")
    print("%s - - - INSTAGRAM TOOL - - - %s" % (fg(207), attr(0)))
    print(" ")
    secim = input("%s[1]- Download Profile Picture\n[2]- Download Post Picture\n[3]- Freeze Account\n[4]- Get Your Follower List\n[5]- Follower Farm\n[6]- unFollow Farm \n[7]- Show Pictures\n[8]- Delete Pictures\n[9]- Exit\n%s \nEnter Number:" % (fg(207), attr(0)))
    if secim == "1":
        username = input("%susername: %s" % (fg(207), attr(0)))
        Instagram.profilephoto(username)
    elif secim == "9":
        print("%sGOODBYE BABE%s" % (fg(207), attr(0)))
        time.sleep(1)
        exit()
    elif secim == "2":
        link = input("%sPicture Link: %s" % (fg(207), attr(0)))
        Instagram.downloadPost(link)
    elif secim == "3":
        username = input("%susername: %s" % (fg(207), attr(0)))
        password = input("%spassword: %s" % (fg(207), attr(0)))
        Instagram.login(username,password)
        Instagram.freezeAccount(password)
    elif secim == "7":
        Instagram.showpic()
    elif secim == "8":
        Instagram.deletepic()
    elif secim == "4":
        username = input("%susername: %s" % (fg(207), attr(0)))
        password = input("%spassword: %s" % (fg(207), attr(0)))
        Instagram.login(username,password)
        Instagram.getFollowers(username)
    elif secim == "5":
        username = input("%sUsername: %s" % (fg(207), attr(0)))
        password = input("%sPassword: %s" % (fg(207), attr(0)))
        target = input("%sTarget account name: %s" % (fg(207), attr(0)))
        total = int(input("%sTotal Follow: %s" % (fg(10), attr(0))))
        Instagram.login(username,password)
        Instagram.navigateFollowers(target)
        Instagram.getUserList(total)
        Instagram.follow()
        Instagram.message()
        Instagram.closeBot()        
    elif secim == "6":
        username = input("%sUsername: %s" % (fg(207), attr(0)))
        password = input("%sPassword: %s" % (fg(207), attr(0)))
        total = int(input("%sTotal unFollow: %s" % (fg(10), attr(0))))
        Instagram.login(username,password)
        Instagram.navigateFollowings(username)
        Instagram.getUserList(total)
        Instagram.unFollow()
        Instagram.message()
        Instagram.closeBot()
