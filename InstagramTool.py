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
        self.browserProfile.add_argument("--headless") # some methods may not work properly with headless - so it's optional
        self.browserProfile.add_argument("--disable-gpu")
        self.browserProfile.add_argument('--mute-audio')
        self.browserProfile.add_argument('window-size=1920,1080')
        self.browserProfile.add_argument('window-position=0,0')
        self.browserProfile.add_argument("--start-maximized")
        self.browserProfile.add_argument("--force-dark-mode")
        self.browserProfile.add_experimental_option(
            "excludeSwitches", ["disable-popup-blocking"])
        self.browserProfile.add_experimental_option(
            'prefs', {"profile.default_content_setting_values.notifications": "2"})
        self.browserProfile.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
        self.browserProfile.add_experimental_option(
            'prefs', {"intl.accept_languages": "en,en_US"})
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
        self.browser.find_element(
            By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div').click()
        time.sleep(7)
        try:
            errmsg = self.browser.find_element(
                By.XPATH, '//*[@id="slfErrorAlert"]')
            print(f"%s {errmsg.text} \n%s" % (fg(1), attr(0)))
            return False
        except:
            return True

    def message(self):
        print("%s\n--> DONE%s" % (fg(1), attr(0)))

    def closeBot(self):
        self.browser.close()
        self.userList = []

    def showImg(self):
        os.system("cls")
        fileName = input("\n%s[post / pp / result] :%s" % (fg(30), attr(0)))
        try:
            img = Image.open(F"{self.imgPath}/{fileName}.png")
            img.show()
        except FileNotFoundError:
            print("%s--> File not found!%s" % (fg(1), attr(0)))

    def deleteImg(self):
        os.system("cls")
        files = ["pp", "post", "result"]
        fileName = input(f"\n%s {files}: %s" %
                         (fg(30), attr(0)))
        if fileName == "all":
            for file in files:
                try:
                    os.remove(f"{self.imgPath}/{file}.png")
                except FileNotFoundError:
                    pass
            print("\n%s--> All files deleted!%s\n" % (fg(2), attr(0)))
        else:
            try:
                os.remove(f"{self.imgPath}/{fileName}.png")
                print("\n%s--> Deleted!%s\n" % (fg(2), attr(0)))
            except FileNotFoundError:
                pass

    def downloadPP(self, username):
        os.system("cls")
        self.browser = webdriver.Chrome(self.drvPath, chrome_options=self.browserProfile)
        self.username = username
        
        print("\n%s--> Processing...%s" % (fg(1), attr(0)))
        self.browser.get(f"https://instabig.net/download-instagram-instadp")
        
        print("\n%s--> Downloading image...\n %s" % (fg(226), attr(0)))
        time.sleep(2)
        self.browser.find_element(By.XPATH, "/html/body/div[1]/div/form/div/input").send_keys(username)
        self.browser.find_element(By.XPATH, "/html/body/div[1]/div/form/div/button").click()
        
        byt = ""
        while byt == "":
            time.sleep(1)
            try:
                byt = self.browser.find_element(By.XPATH, "//*[@class='imgInstadp']")
            except:
                pass

        src = byt.get_attribute("src")
        time.sleep(1)
        urllib.request.urlretrieve(src, f"{self.imgPath}/pp.png")
        print("%s--> Downloaded!%s" % (fg(46), attr(0)))

    def downloadPost(self, link):
        os.system("cls")
        self.link = link
        print("%s---> Loading...%s" % (fg(2), attr(0)))
        self.browser = webdriver.Chrome(
            self.drvPath, chrome_options=self.browserProfile)
        self.browser.get(f"{link}media/?size=l")
        time.sleep(2)
        src = self.browser.find_element(By.TAG_NAME, "img").get_attribute('src')
        urllib.request.urlretrieve(src, f"{self.imgPath}/post.png")
        print("%s---> Downloaded!%s" % (fg(2), attr(0)))

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

    # fmt: off
    def navigateTo(self, user, path):
        self.browser.get(f'https://www.instagram.com/{user}')
        print(f"%s--> Navigating to {path}\n%s" % (fg(61), attr(0)))
        time.sleep(3)
        self.browser.find_element(By.XPATH, f'//*[@href="/{user}/{path}/"]').click()
        time.sleep(2)

    def userAction(self, action):
        count = 0
        for user in self.userList:
            os.system("cls")
            print(
                f"%s--> Processing\n--> Total {action}: {count}/{len(self.userList)} %s" % (fg(43), attr(0)))
            self.browser.get(user)

            # Wait for 15 seconds to avoid Instagram blocking actions
            # You can change the time to 30 seconds or more in case you get blocked
            # Please note that the more you increase the time, the more time it will take to finish the process
            # Please don't use a time less than 15 seconds
            for wait in range(16):
                print(f"%s--> {15-wait} seconds left to {action.lower()} next user... %s" %
                      (fg(2), attr(0)), end="\r")
                time.sleep(1)

            try:
                if action == "Follow":
                    self.browser.execute_script(_scripts.followUser)
                else:
                    self.browser.execute_script(_scripts.unfollowUser)
            except:
                print(
                    f"%s\n --> Connection speed getting slower. Skipping... %s" % (fg(1), attr(0)))
            time.sleep(1.5)
            try:
                self.browser.find_element(By.TAG_NAME, "h3")
                print(
                    f"%s\n --> Instagram blocked {action} actions. Try again later. %s" % (fg(1), attr(0)))
                break
            except:
                time.sleep(1.5)
                count += 1

    # Followings List
    def getFollowings(self, total):
        time.sleep(5)

        while True:
            self.browser.execute_script(_scripts.scrollScript)
            time.sleep(2)

            newCount = len(self.browser.find_elements(
                By.XPATH, "//*[@aria-labelledby]"))
            os.system("cls")
            print(
                f"%s Total Collected: {newCount}/{total} %s" % (fg(10), attr(0)))

            if newCount <= 1:
                break

            if newCount < total:
                time.sleep(0.5)
            else:
                break

        followers = self.browser.find_elements(
            By.XPATH, "//*[@aria-labelledby]")
        self.userList = []

        i = 0
        for user in followers:
            link = user.find_element(By.TAG_NAME, "a").get_attribute("href")
            self.userList.append(link)
            i += 1
            if i >= total:
                break

    # Follower List
    def getFollowers(self, username):
        os.system('cls')
        self.browser.get(f"https://www.instagram.com/{username}/followers")
        time.sleep(3)

        print("%sCounting Followers%s" % (fg(2), attr(0)))

        # dialog = self.browser.find_element(By.XPATH, "//*[@role='dialog']")
        counterFollowers = len(self.browser.find_elements(
            By.XPATH, "//*[@aria-labelledby]"))
        print(f"First Time Counting Followers: {counterFollowers}")

        while True:
            self.browser.execute_script(_scripts.scrollScript)
            time.sleep(2)

            newCount = len(self.browser.find_elements(
                By.XPATH, "//*[@aria-labelledby]"))
            os.system("cls")

            if counterFollowers != newCount:
                counterFollowers = newCount
                os.system('cls')
                print(f"%sCollected Followers: {newCount}%s" % (
                    fg(10), attr(0)))
            else:
                break

        print("%sSaving... %s" % (fg(2), attr(0)))

        try:
            totalFollowers = self.browser.find_elements(
                By.XPATH, "//*[@aria-labelledby]")  # //*[@aria-labelledby]

            Flist = []
            i = 0
            for users in totalFollowers:
                i += 1
                if i == counterFollowers:
                    break

                link = users.find_element(
                    By.TAG_NAME, "a").get_attribute("href")
                Flist.append(link)
                with open("followers.txt", "w", encoding="utf-8") as file:
                    for item in Flist:
                        file.write(item + "\n")
        except:
            print("%sSomething went wrong while saving followers. Please try again. %s" % (
                fg(1), attr(0)))

        print("%sDone! All followers successfully saved to 'followers.txt' file. %s" % (
            fg(2), attr(0)))

    # ---------------- DEPRECATED ----------------
    # def removeRequests(self, threshold):
    #     os.system('cls')
    #     print("%s--> Navigating to requested accounts list \n%s" % (fg(61), attr(0)))

    #     self.browser.get(f"https://www.instagram.com/accounts/access_tool/current_follow_requests")
    #     time.sleep(3)

    #     while True:
    #         time.sleep(2)

    #         newCount = self.browser.execute_script('return document.querySelectorAll("article div").length')

    #         if (newCount == threshold):
    #             break

    #         os.system("cls")
    #         print(f"%s Total Collected: {newCount}/{total}%s " % (fg(10), attr(0)))

    #         try:
    #             self.browser.find_element(By.XPATH, '//*["article"]/main/button').click()
    #         except:
    #             break

    #     requestedAccountNames = self.browser.execute_script('return document.querySelectorAll("article div")')
    #     print(f"%s \n--> Generating links... %s" % (fg(10), attr(0)))
    #     self.userList = []

    #     for user in requestedAccountNames:
    #         username = user.text
    #         self.userList.append(f"https://www.instagram.com/{username}/")


Instagram = Instagram()

while True:
    print("%s\n - - - INSTAGRAM TOOL - - - \n %s" % (fg(207), attr(0)))
    opt = input("%s"
        "[0] - Download Profile Picture\n"
        "[1] - Download Post Picture\n"
        "[2] - Freeze Account\n"
        "[3] - Get Your Follower List\n"
        "[4] - Follower Farm\n"
        "[5] - unFollow Farm \n"
        "[6] - Show Pictures\n"
        "[7] - Delete Pictures\n"
        "[8] - Remove Requests\n"
        "[9] - Exit \n\n"
        "%sEnter Number:""" % (fg(207), attr(0)))
    if opt == "0":
        # Download Profile Picture
        username = input("%susername: %s" % (fg(207), attr(0)))
        Instagram.downloadPP(username)
        Instagram.closeBot()
    elif opt == "9":
        exit()
    elif opt == "1":
        # Download Post Picture
        link = input("%sPost Link: %s" % (fg(207), attr(0)))
        Instagram.downloadPost(link)
        Instagram.closeBot()
    elif opt == "2":
        # Freeze Account
        username = _loginInfo.username if _loginInfo.username != "" else input(
            "%susername: %s" % (fg(207), attr(0)))
        password = _loginInfo.password if _loginInfo.password != "" else input(
            "%spassword: %s" % (fg(207), attr(0)))
        res = Instagram.login(username, password)
        if res:
            Instagram.freezeAccount(password)
            Instagram.closeBot()
        else:
            Instagram.closeBot()
    elif opt == "6":
        # Show Pictures
        Instagram.showImg()
    elif opt == "7":
        # Delete Pictures
        Instagram.deleteImg()
    elif opt == "3":
        # Get Followers
        username = _loginInfo.username if _loginInfo.username != "" else input(
            "%susername: %s" % (fg(207), attr(0)))
        password = _loginInfo.password if _loginInfo.password != "" else input(
            "%spassword: %s" % (fg(207), attr(0)))
        res = Instagram.login(username, password)
        if res:
            Instagram.getFollowers(username)
            Instagram.closeBot()
        else:
            Instagram.closeBot()
    elif opt == "4":
        # Follower Farm
        username = _loginInfo.username if _loginInfo.username != "" else input(
            "%susername: %s" % (fg(207), attr(0)))
        password = _loginInfo.password if _loginInfo.password != "" else input(
            "%spassword: %s" % (fg(207), attr(0)))
        target = input("%sTarget account name: %s" % (fg(207), attr(0)))
        total = int(input("%sTotal Follow: %s" % (fg(10), attr(0))))
        res = Instagram.login(username, password)
        if res:
            Instagram.navigateTo(target, "followers")
            Instagram.getFollowings(total)
            Instagram.userAction("Follow")
            Instagram.message()
            Instagram.closeBot()
        else:
            Instagram.closeBot()
    elif opt == "5":
        # Unfollow Farm
        username = _loginInfo.username if _loginInfo.username != "" else input(
            "%susername: %s" % (fg(207), attr(0)))
        password = _loginInfo.password if _loginInfo.password != "" else input(
            "%spassword: %s" % (fg(207), attr(0)))
        total = int(input("%sTotal unFollow: %s" % (fg(10), attr(0))))
        res = Instagram.login(username, password)
        if res:
            Instagram.navigateTo(username, "following")
            Instagram.getFollowings(total)
            Instagram.userAction("unFollow")
            Instagram.message()
            Instagram.closeBot()
        else:
            Instagram.closeBot()
    elif opt == "8":
        # Remove Requests
        os.system("cls")
        print("%s\n --> DEPRECATED - Instagram doesn't show requested accounts anymore. %s" %
              (fg(2), attr(0)))
        # username = _loginInfo.username if _loginInfo.username != "" else input("%susername: %s" % (fg(207), attr(0)))
        # password = _loginInfo.password if _loginInfo.password != "" else input("%spassword: %s" % (fg(207), attr(0)))
        # print("%s--> Determine user threshold for less wait time (ex. 100) %s" % (fg(207), attr(0)))
        # threshold = input("%sThreshold: %s" % (fg(207), attr(0)))
        # res = Instagram.login(username, password)
        # if res:
        #     Instagram.removeRequests(threshold)
        #     Instagram.unFollow()
        #     Instagram.message()
        #     Instagram.closeBot()
        # else:
        #     Instagram.closeBot()
