from colored import fg, attr
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request
import warnings
import time
import os
from PIL import Image
import _loginInfo 
import _scripts

warnings.filterwarnings("ignore", category=DeprecationWarning)

class Instagram:

    def __init__(self):
        self.drvPath = "./driver/chromedriver.exe"
        self.imgPath = "./images"
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_argument("--lang=en")
        self.browserProfile.add_argument("--log-level=3")
        self.browserProfile.add_argument('--hide-scrollbars')
        self.browserProfile.add_argument("--headless")    # ---> some methods may not work properly with headless - so it's optional
        self.browserProfile.add_argument("--disable-gpu")
        self.browserProfile.add_argument('--mute-audio')
        self.browserProfile.add_argument('window-size=1920,1080')
        self.browserProfile.add_argument('window-position=0,0')
        self.browserProfile.add_argument("--start-maximized")
        self.browserProfile.add_argument("--force-dark-mode")
        self.browserProfile.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
        self.browserProfile.add_experimental_option('prefs', {"profile.default_content_setting_values.notifications" : "2"})
        self.browserProfile.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.browserProfile.add_experimental_option('prefs', {"intl.accept_languages": "en,en_US"})
        self.username = _loginInfo.username
        self.password = _loginInfo.password

    def login(self, username, password):
        os.system('cls')
        self.browser = webdriver.Chrome(
            self.drvPath, chrome_options=self.browserProfile)
        print("%s--> Login in\n%s" % (fg(61), attr(0)))
        self.username = username
        self.password = password
        time.sleep(2)
        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)
        self.browser.find_element(By.NAME, 'username').send_keys(self.username)
        self.browser.find_element(By.NAME, 'password').send_keys(self.password)
        self.browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div').click()
        time.sleep(7)
        try:
            errmsg = self.browser.find_element(By.XPATH, '//*[@id="slfErrorAlert"]')
            print(f"%s {errmsg.text} \n%s" % (fg(1), attr(0)))
            return False
        except:
            return True
            
    def message(self):
        print("%s\n--> DONE%s" % (fg(1), attr(0)))

    def closeBot(self):
        self.browser.close()
        self.mainList = []
        
    def showpic(self):
        os.system("cls")
        show = input("\n%s[post / pp / result] :%s" % (fg(30), attr(0)))
        if show == "pp":
            try:
                img = Image.open(F"{self.imgPath}/igpp.png")
                img.show()
            except FileNotFoundError:
                print("\n%s---> There is not screenshot yet%s\n" %
                      (fg(1), attr(0)))
        elif show == "post":
            try:
                img = Image.open(F"{self.imgPath}/igpost.png")
                img.show()
            except FileNotFoundError:
                print("\n%s---> There is not screenshot yet%s\n" %
                      (fg(1), attr(0)))
        elif show == "result":
            try:
                img = Image.open(F"{self.imgPath}/result.png")
                img.show()
            except FileNotFoundError:
                print("\n%s---> There is not screenshot yet%s\n" %
                      (fg(1), attr(0)))

    def deletepic(self):
        os.system("cls")
        delete = input("\n%s[post / pp / result / all] :%s" %
                       (fg(30), attr(0)))
        if delete == "pp":
            try:
                os.remove(f"{self.imgPath}/igpp.png")
                print("\n%s---> Deleted!%s\n" % (fg(2), attr(0)))
            except FileNotFoundError:
                print("\n%s---> There is not screenshot yet%s\n" %
                      (fg(2), attr(0)))
        elif delete == "post":
            try:
                os.remove(f"{self.imgPath}/igpost.png")
                print("\n%s---> Deleted!%s\n" % (fg(2), attr(0)))
            except FileNotFoundError:
                print("\n%s---> There is not screenshot yet%s\n" %
                      (fg(2), attr(0)))
        elif delete == "result":
            try:
                os.remove(f"{self.imgPath}/igpost.png")
                print("\n%s---> Deleted!%s\n" % (fg(2), attr(0)))
            except FileNotFoundError:
                print("\n%s---> There is not screenshot yet%s\n" %
                      (fg(2), attr(0)))
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

    def profilephoto(self, username):
        self.browser = webdriver.Chrome(
            self.drvPath, chrome_options=self.browserProfile)
        os.system("cls")
        self.username = username
        print("\n%s--> Processing...%s" % (fg(1), attr(0)))
        self.browser.get(f"https://instabig.net/fullsize/{self.username}")
        print("\n%s--> Searching image...\n %s" % (fg(226), attr(0)))
        time.sleep(2)
        byt = self.browser.find_element(By.XPATH, '//*[@id="imgBigPP"]')
        src = byt.get_attribute("src")
        time.sleep(1)
        urllib.request.urlretrieve(src, f"{self.imgPath}/igpp.png")
        print("%s--> Downloaded!%s" % (fg(46), attr(0)))

    def downloadPost(self, link):
        os.system("cls")
        self.link = link
        print("%s---> Loading...%s" % (fg(2), attr(0)))
        self.browser = webdriver.Chrome(
            self.drvPath, chrome_options=self.browserProfile)
        self.browser.get(link)
        time.sleep(2)
        loc = self.browser.find_elements(By.TAG_NAME, "img")[1]
        img = loc.find_element(By.XPATH, "//div/img")
        src = img.get_attribute('src')
        urllib.request.urlretrieve(src, f"{self.imgPath}/igpost.png")
        print("%s---> DONE!%s" % (fg(2), attr(0)))

    def freezeAccount(self, password):
        os.system("cls")
        print("%s---> Account freezing%s\n" % (fg(2), attr(0)))
        self.browser.get(
            'https://www.instagram.com/accounts/remove/request/temporary/')
        time.sleep(2)
        self.browser.find_element(
            By.XPATH, '//*[@id="deletion-reason"]').click()
        time.sleep(2)
        self.browser.find_element(
            By.XPATH, "//option[@value='need-break']").click()
        self.browser.find_element(
            By.XPATH, '//*[@id="password"]').send_keys(password)
        time.sleep(2)
        self.browser.find_element(
            By.CSS_SELECTOR, 'article form button').click()
        time.sleep(2)
        self.browser.find_element(
            By.CSS_SELECTOR, 'article form div div button').click()
        print("%s---> Results coming%s\n" % (fg(2), attr(0)))
        time.sleep(2)
        self.browser.save_screenshot(f"{self.imgPath}/result.png")
        img = Image.open(f"{self.imgPath}/result.png")
        time.sleep(2)
        img.show()

    def navigateFollowers(self, user):
        print("%s--> Navigating Followers\n%s" % (fg(61), attr(0)))
        time.sleep(3)
        self.browser.get(f'https://www.instagram.com/{user}/followers')
        time.sleep(2)

    def navigateFollowings(self, user):
        print("%s--> Navigating Followings\n%s" % (fg(61), attr(0)))
        time.sleep(3)
        self.browser.get(f'https://www.instagram.com/{user}/following')
        time.sleep(2)
        
    def follow(self):
        count = 0
        for user in self.mainList:
            os.system("cls")
            print(f"%s--> Processing:\n--> Follow count: {count} %s" %(fg(43), attr(0)))
            self.browser.get(user)
            time.sleep(2)
            try:
                self.browser.execute_script(_scripts.followUser)
            except:
                print(f"%s\n --> Connection speed getting slower. Skipping... %s" %(fg(1), attr(0)))
            time.sleep(2)
            try: 
                self.browser.find_element(By.TAG_NAME, "h3")
                print(f"%s\n --> Instagram blocked Follow actions. Try again later. %s" %(fg(1), attr(0)))
                break
            except:
                time.sleep(1)
                count+=1

    def unFollow(self):
        count = 0
        for user in self.mainList:
            os.system("cls")
            print(f"%s--> Processing:\n--> unFollow count: {count} %s" %(fg(43), attr(0)))
            self.browser.get(user)
            time.sleep(2)
            try:
                self.browser.execute_script(_scripts.unFollowUser)
            except:
                print(f"%s\n --> Connection speed getting slower. Skipping... %s" %(fg(1), attr(0)))
            time.sleep(2)
            self.browser.find_element(By.XPATH, '//button[text()="Unfollow"]').click()
            time.sleep(1)
            try: 
                self.browser.find_element(By.TAG_NAME, "h3")
                print(f"%s\n --> Instagram blocked unFollow actions. Try again later. %s" %(fg(1), attr(0)))
                break
            except:
                time.sleep(1)
                count+=1
        
    def getUserList(self, total):
        time.sleep(5)
        dialog = self.browser.find_element(By.XPATH, "//*[@class='_aano']/div/div")

        while True:
            self.browser.execute_script(_scripts.scrollScript)
            time.sleep(2)
            
            newCount = len(dialog.find_elements(By.XPATH, "//div[@aria-labelledby]"))
            os.system("cls")
            print(f"%sTotal Collected: {newCount}%s" % (fg(10), attr(0)))
        
            if newCount <= 1:
                break

            if newCount < total:
                time.sleep(0.5)
            else:
                break

        followers = dialog.find_elements(By.XPATH, "//div[@aria-labelledby]")
        self.mainList = []

        i = 0
        for user in followers:
            link = user.find_element(By.TAG_NAME, "a").get_attribute("href")
            self.mainList.append(link)
            i += 1
            if i >= total:
                break
        

    def getFollowers(self, username):
        os.system('cls')
        self.browser.get(f"https://www.instagram.com/{username}/followers")
        time.sleep(3)

        print("%sCounting Followers%s" % (fg(2), attr(0)))

        dialog = self.browser.find_element(By.XPATH, "//*[@class='_aano']/div/div")
        CurrentFollowers = len(dialog.find_elements(By.XPATH, "./child::*"))
        print(f"First Time Counting Followers: {CurrentFollowers}")
        
        while True:
            self.browser.execute_script(_scripts.scrollScript)
            time.sleep(2)
            
            newCount = len(dialog.find_elements(By.XPATH, "./child::*"))
            os.system("cls")

            if CurrentFollowers != newCount:
                CurrentFollowers = newCount
                os.system('cls')
                print(f"%sCollected Followers: {newCount}%s" % (fg(10), attr(0)))
            else:
                break
        
        print("%sSaving... %s" % (fg(2), attr(0)))
        
        try:
            totalFollowers = dialog.find_elements(By.XPATH, "./child::*")

            Flist = []
            i = 0
            for users in totalFollowers:
                i += 1
                if i == CurrentFollowers:
                    break

                link = users.find_element(By.TAG_NAME, "a").get_attribute("href")
                Flist.append(link)
                with open("followers.txt", "w", encoding="utf-8") as file:
                    for item in Flist:
                        file.write(item + "\n")
        except:
            print("%sSomething gone wrong while saving followers. Please try again. %s" % (fg(1), attr(0)))
            
        print("%sDone!\nAll Followers Saved to 'followers.txt' file. %s" % (fg(2), attr(0)))

    def removeRequests(self):
        os.system('cls')
        print("%s--> Navigating to requested accounts list \n%s" % (fg(61), attr(0)))

        self.browser.get(f"https://www.instagram.com/accounts/access_tool/current_follow_requests")
        time.sleep(3)

        while True:
            time.sleep(2)
            
            newCount = self.browser.execute_script('return document.querySelectorAll("article div").length')

            os.system("cls")
            print(f"%sTotal Collected: {newCount}%s" % (fg(10), attr(0)))

            try:
                self.browser.find_element(By.XPATH, '//*["article"]/main/button').click()
            except:
                break
        
        requestedAccountNames = self.browser.execute_script('return document.querySelectorAll("article div")')
        print(f"%s \n--> Generating links... %s" % (fg(10), attr(0)))
        self.mainList = []

        for user in requestedAccountNames:
            username = user.text
            self.mainList.append(f"https://www.instagram.com/{username}/")

Instagram = Instagram()

while True:
    print("")
    print("%s - - - INSTAGRAM TOOL - - - %s" % (fg(207), attr(0)))
    print(" ")
    opt = input("%s[0]- Download Profile Picture\n[1]- Download Post Picture\n[2]- Freeze Account\n[3]- Get Your Follower List\n[4]- Follower Farm\n[5]- unFollow Farm \n[6]- Show Pictures\n[7]- Delete Pictures\n[8]- Remove Requests\n[9]- Exit \n%s \nEnter Number:" % (fg(207), attr(0)))
    if opt == "0":
        username = input("%susername: %s" % (fg(207), attr(0)))
        Instagram.profilephoto(username)
        Instagram.closeBot()
    elif opt == "9":
        exit()
    elif opt == "1":
        link = input("%Post Link: %s" % (fg(207), attr(0)))
        Instagram.downloadPost(link)
        Instagram.closeBot()
    elif opt == "2":
        username = _loginInfo.username if _loginInfo.username != "" else input("%susername: %s" % (fg(207), attr(0))) 
        password = _loginInfo.password if _loginInfo.password != "" else input("%spassword: %s" % (fg(207), attr(0)))
        res = Instagram.login(username, password)
        if res:
            Instagram.freezeAccount(password)
            Instagram.closeBot()
        else:
            Instagram.closeBot()
    elif opt == "6":
        Instagram.showpic()
    elif opt == "7":
        Instagram.deletepic()
    elif opt == "3":
        username = _loginInfo.username if _loginInfo.username != "" else input("%susername: %s" % (fg(207), attr(0))) 
        password = _loginInfo.password if _loginInfo.password != "" else input("%spassword: %s" % (fg(207), attr(0)))
        res = Instagram.login(username, password)
        if res:
            Instagram.getFollowers(username)
            Instagram.closeBot()
        else:
            Instagram.closeBot()
    elif opt == "4":
        username = _loginInfo.username if _loginInfo.username != "" else input("%susername: %s" % (fg(207), attr(0))) 
        password = _loginInfo.password if _loginInfo.password != "" else input("%spassword: %s" % (fg(207), attr(0)))
        target = input("%sTarget account name: %s" % (fg(207), attr(0)))
        total = int(input("%sTotal Follow: %s" % (fg(10), attr(0))))
        res = Instagram.login(username, password)
        if res:
            Instagram.navigateFollowers(target)
            Instagram.getUserList(total)
            Instagram.follow()
            Instagram.message()
            Instagram.closeBot()
        else:
            Instagram.closeBot()
    elif opt == "5":
        username = _loginInfo.username if _loginInfo.username != "" else input("%susername: %s" % (fg(207), attr(0))) 
        password = _loginInfo.password if _loginInfo.password != "" else input("%spassword: %s" % (fg(207), attr(0)))
        total = int(input("%sTotal unFollow: %s" % (fg(10), attr(0))))
        res = Instagram.login(username, password)
        if res:
            Instagram.navigateFollowings(username)
            Instagram.getUserList(total)
            Instagram.unFollow()
            Instagram.message()
            Instagram.closeBot()
        else:
            Instagram.closeBot()
    elif opt == "8":
        username = _loginInfo.username if _loginInfo.username != "" else input("%susername: %s" % (fg(207), attr(0))) 
        password = _loginInfo.password if _loginInfo.password != "" else input("%spassword: %s" % (fg(207), attr(0)))
        res = Instagram.login(username, password)
        if res:
            Instagram.removeRequests()
            Instagram.unFollow()
            Instagram.message()
            Instagram.closeBot()
        else:
            Instagram.closeBot()