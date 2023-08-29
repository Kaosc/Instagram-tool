from colored import fg, attr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import urllib.request
import warnings
import time
import os
import requests
from PIL import Image
import _loginInfo
import _scripts
import json

warnings.filterwarnings("ignore", category=DeprecationWarning)

class Instagram:
    def __init__(self):
        self.drvPath = "./driver/chromedriver.exe"
        self.imgPath = "./images"
        self.userList = []
        self.pendingFollowRequestHrefs = []
        self.service = Service(self.drvPath)
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_argument("--lang=en")
        self.browserProfile.add_argument("--log-level=3")
        self.browserProfile.add_argument('--hide-scrollbars')
        self.browserProfile.add_argument("--headless")
        self.browserProfile.add_argument("--disable-gpu")
        self.browserProfile.add_argument('--mute-audio')
        self.browserProfile.add_argument('window-size=1920,1080')
        self.browserProfile.add_argument('window-position=0,0')
        self.browserProfile.add_argument("--start-maximized")
        self.browserProfile.add_argument("--force-dark-mode")
        self.browserProfile.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
        self.browserProfile.add_experimental_option('prefs', {"profile.default_content_setting_values.notifications": "2"})
        self.browserProfile.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.browserProfile.add_experimental_option('prefs', {"intl.accept_languages": "en,en_US"})
        self.browser = webdriver.Chrome(service=self.service, options=self.browserProfile)

    def createImagePath(self):
        # create images folder if not exists
        if not os.path.exists(self.imgPath):
            os.makedirs(self.imgPath)

    def getTotalFileSum(self, path):
        total = 0
        for root, dirs, files in os.walk(path):
            total += len(files)

        if total == 0:
            return ""
        else:
            return total

    def login(self, username, password):
        os.system("cls")

        print("%s⊳ Logging in\n%s" % (fg(61), attr(0)))
        time.sleep(2)
        
        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)
        
        self.browser.find_element(By.NAME, 'username').send_keys(username)
        self.browser.find_element(By.NAME, 'password').send_keys(password)
        self.browser.find_element(By.XPATH, '//*[@type="submit"]').click()
        time.sleep(7)
        
        try:
            errmsg = self.browser.find_element(By.XPATH, '//*[@id="slfErrorAlert"]')
            print(f"%s {errmsg.text} \n%s" % (fg(1), attr(0)))
            return False
        except:
            return True

    def message(self):
        print("%s\n⊳ DONE%s" % (fg(1), attr(0)))

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
            print("%s⊳ File not found!%s" % (fg(1), attr(0)))

    def deleteImg(self):
        os.system("cls")
        files = ["pp", "post", "result"]
        fileName = input(f"\n%s {files}: %s" % (fg(30), attr(0)))

        if fileName == "all":
            for file in files:
                try:
                    os.remove(f"{self.imgPath}/{file}.png")
                except FileNotFoundError:
                    pass
            print("\n%s⊳ All files deleted!%s\n" % (fg(2), attr(0)))
        else:
            try:
                os.remove(f"{self.imgPath}/{fileName}.png")
                print("\n%s⊳ Deleted!%s\n" % (fg(2), attr(0)))
            except FileNotFoundError:
                pass

    def downloadPP(self, username):
        os.system("cls")

        print("\n%s⊳ Processing...%s" % (fg(1), attr(0)))

        url = f"https://www.instagram.com/{username}/?__a=1&__d=1"
        pic = requests.get(url).json()["graphql"]["user"]["profile_pic_url_hd"]

        # create images folder if not exists
        self.createImagePath()
        fileNum = self.getTotalFileSum(self.imgPath)

        urllib.request.urlretrieve(pic, f"{self.imgPath}/pp{fileNum}.png")

        print("%s⊳ Downloaded!%s" % (fg(46), attr(0)))

    def downloadPost(self, link = ""):
        os.system("cls")
        print("%s-⊳ Downloading...%s" % (fg(2), attr(0)))

        # if link is not a post link, convert it to post link
        postId = link.split("/")[-2]

        self.browser.get(f"https://www.instagram.com/p/{postId}/media/?size=l")
        time.sleep(2)

        src = self.browser.find_element(By.TAG_NAME, "img").get_attribute('src')

        # create images folder if not exists
        self.createImagePath()
        fileNum = self.getTotalFileSum(self.imgPath)
        
        urllib.request.urlretrieve(src, f"{self.imgPath}/post{fileNum}.png")

        print("%s-⊳ Downloaded!%s" % (fg(2), attr(0)))

    def freezeAccount(self, password):
        os.system("cls")
        print("%s-⊳ Account freezing%s\n" % (fg(2), attr(0)))
        self.browser.get('https://www.instagram.com/accounts/remove/request/temporary/')
        time.sleep(2)
        self.browser.find_element(By.XPATH, '//*[@id="deletion-reason"]').click()
        time.sleep(2)
        self.browser.find_element(By.XPATH, "//option[@value='need-break']").click()
        self.browser.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
        time.sleep(2)
        self.browser.find_element(By.CSS_SELECTOR, 'article form button').click()
        time.sleep(2)
        self.browser.find_element(By.CSS_SELECTOR, 'article form div div button').click()

        print("%s-⊳ Results coming%s\n" % (fg(2), attr(0)))
        time.sleep(2)

        self.browser.save_screenshot(f"{self.imgPath}/result.png")
        img = Image.open(f"{self.imgPath}/result.png")
        time.sleep(2)
        
        img.show()

    def navigateTo(self, user, path):
        self.browser.get(f'https://www.instagram.com/{user}')
        print(f"%s⊳ Navigating to {path}\n%s" % (fg(61), attr(0)))
        time.sleep(3)
        
        try: 
            self.browser.find_element(By.XPATH, f'//*[@href="/{user}/{path}/"]').click()
            time.sleep(2)
            return True
        except:
            print(f"%s⊳ {user} does not exist!%s" % (fg(1), attr(0)))
            return False
        
    def userAction(self, action):
        count = 0
        hrefs = action == "removeRequest" and self.pendingFollowRequestHrefs or self.userList
        
        for user in hrefs:
            os.system("cls")

            skip = True
            
            print(f"%s⊳ Total {action}ed: {count}/{len(hrefs)} %s" % (fg(43), attr(0)))
            self.browser.get(user)

            # Check page load block
            try:
                time.sleep(1)
                isBlocked = self.browser.find_element(By.XPATH, "//*[@aria-label='Error']")
                if isBlocked:
                    print(f"%s\n ⊳ Instagram blocked {action} actions. Try again later. %s" % (fg(1), attr(0)))
                    self.closeBot()
                    break
            except:
                pass

            # Execute follow/unfollow aciton
            try:
                time.sleep(2)



                if action == "Follow":
                    ################################
                    ############ Follow ############
                    ################################

                    # This will skip ["Requested", "Following", "Follow Back"] buttons
                    try:
                        followButton = self.browser.find_element(By.XPATH, "//header//*[@type='button']//*[contains(text(), 'Follow')]")
                        if followButton.text == "Follow":
                            followButton.click()
                            skip = False
                    except:
                        pass

                elif action == "removeRequest":
                    #################################
                    ######### removeRequest #########
                    #################################

                    # Open popup dialog 
                    try:
                        popupButton = self.browser.find_element(By.XPATH, "//header//*[@type='button']//*[contains(text(), 'Requested')]")
                        if popupButton.text == "Requested":
                            if popupButton.text == "Requested":
                                popupButton.click()
                                skip = False
                    except:
                        pass

                    # Click unfollow button in popup dialog
                    time.sleep(1.5)
                    try:
                        unFollowButton = self.browser.find_element(By.XPATH, "//*/button[contains(text(), 'Unfollow')]")
                        if unFollowButton.text == "Unfollow":
                            unFollowButton.click()
                            skip = False
                    except:
                        pass
                else:
                    ################################
                    ########### unFollow ###########
                    ################################

                    # Open popup dialog 
                    try:
                        popupButton = self.browser.find_element(By.XPATH, "//header//*[@type='button']//*[contains(text(), 'Following')]")
                        if popupButton.text == "Following":
                            if popupButton.text == "Following":
                                popupButton.click()
                                skip = False
                    except:
                        pass

                    # Click unfollow button in popup dialog
                    time.sleep(1.5)
                    try:
                        unFollowButton = self.browser.find_element(By.XPATH, "//*/div[@role='button']//*[contains(text(), 'Unfollow')]")
                        if unFollowButton.text == "Unfollow":
                            unFollowButton.click()
                            skip = False
                    except:
                        pass
            except Exception as e:
                print(f"%s\n ⊳ Connection speed getting slower. Skipping... %s" % (fg(1), attr(0)))
                print(e)
            
            # Check action block
            try:
                time.sleep(1.5)
                self.browser.find_element(By.TAG_NAME, "h3")
                print(f"%s\n ⊳ Instagram blocked {action} actions. Try again later. %s" % (fg(1), attr(0)))
                break
            except:
                pass

            count += 1

            # Wait for 20 seconds to avoid Instagram blocking actions
            # You can change the time to 30 seconds or more in case you get blocked
            # Please note that the more you increase the time, the more time it will take to finish the process
            # Please don't use a time less than 15 seconds
            if skip:
                print(f"%s\n ⊳ Skipping {action} action cause it's already done. %s" % (fg(1), attr(0)))
                time.sleep(1)
            else:
                sleepTime = action == "Follow" and 20 or 25
                for wait in range(sleepTime):
                    print(f"%s⊳ {sleepTime-wait} seconds left to {action.lower()} next user... %s" % (fg(2), attr(0)), end="\r")
                    time.sleep(1)

    # Followings List
    def getFollowings(self, total):
        time.sleep(5)

        while True:
            self.browser.execute_script(_scripts.scrollScript)
            time.sleep(2)

            newCount = len(self.browser.find_elements(By.XPATH, "//*[@class='_aano']/div/div/div"))
            os.system("cls")

            print(f"%s Total Collected: {newCount}/{total} %s" % (fg(10), attr(0)))

            if newCount <= 1:
                break

            if newCount < total:
                time.sleep(0.5)
            else:
                break

        followers = self.browser.find_elements(By.XPATH, "//*[@class='_aano']/div/div/div")
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

        counterFollowers = len(self.browser.find_elements(By.XPATH, "//*[@class='_aano']/div/div/div"))
        print(f"First Time Counting Followers: {counterFollowers}")

        while True:
            self.browser.execute_script(_scripts.scrollScript)
            time.sleep(2)

            newCount = len(self.browser.find_elements(By.XPATH, "//*[@class='_aano']/div/div/div"))
            os.system("cls")

            if counterFollowers != newCount:
                counterFollowers = newCount
                os.system('cls')
                print(f"%sCollected Followers: {newCount}%s" % (fg(10), attr(0)))
            else:
                break

        print("%sSaving... %s" % (fg(2), attr(0)))

        try:
            totalFollowers = self.browser.find_elements(By.XPATH, "//*[@class='_aano']/div/div/div")

            Flist = []
            i = 0
            for users in totalFollowers:
                i += 1
                if i == counterFollowers:
                    break

                link = users.find_element(By.TAG_NAME, "a").get_attribute("href")
                Flist.append(link)
                with open("followers.txt", "w", encoding="utf-8") as file:
                    for item in Flist:
                        file.write(item + "\n")
        except:
            print("%sSomething went wrong while saving followers. Please try again. %s" % (fg(1), attr(0)))

        print("%sDone! All followers successfully saved to 'followers.txt' file. %s" % (fg(2), attr(0)))

    def removeRequests(self):
        os.system('cls')
        print("%s⊳ Importing data from 'pending_follow_requests.json' file... %s" % (fg(61), attr(0)))

        # Importing data from 'pending_follow_requests.json' file
        try:
            f = open('data/pending_follow_requests.json')
            data = json.load(f)
            for i in data['relationships_follow_requests_sent']:
                self.pendingFollowRequestHrefs.append(i['string_list_data'][0]['href'])
            f.close()
        except:
            print("%s⊳ Something went wrong while importing data from 'pending_follow_requests.json' file. Please make sure the file exists and meets the requirements. read the README.md file for more information. %s" % (fg(1), attr(0)))
            return

        # Removing requests
        print("%s⊳ Removing requests... %s" % (fg(61), attr(0)))
        self.userAction("removeRequest")

Instagram = Instagram()

while True:
    print("%s\n∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴%s" % (fg(171), attr(0)))
    print("%s∴∵∴∵∴∵ INSTAGRAM TOOL ∴∵∴∵∴∵∴%s" % (fg(171), attr(0)))
    print("%s∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴\n %s" % (fg(171), attr(0)))
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
        "⊳ ENTER NUMBER: %s""" % (fg(171), attr(0)))
    
    if opt == "0":
        # Download Profile Picture
        username = input("%susername: %s" % (fg(207), attr(0)))
        Instagram.downloadPP(username)
        Instagram.closeBot()
    elif opt == "9":
        exit()
        Instagram.closeBot()
    elif opt == "1":
        # Download Post Picture
        link = input("%sPost Link: %s" % (fg(207), attr(0)))
        Instagram.downloadPost(link)
        Instagram.closeBot()
    elif opt == "2":
        # Freeze Account
        username = _loginInfo.username if _loginInfo.username != "" else input("%susername: %s" % (fg(207), attr(0)))
        password = _loginInfo.password if _loginInfo.password != "" else input("%spassword: %s" % (fg(207), attr(0)))
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
        username = _loginInfo.username if _loginInfo.username != "" else input("%susername: %s" % (fg(207), attr(0)))
        password = _loginInfo.password if _loginInfo.password != "" else input("%spassword: %s" % (fg(207), attr(0)))
        res = Instagram.login(username, password)
        if res:
            Instagram.getFollowers(username)
            Instagram.closeBot()
        else:
            Instagram.closeBot()
    elif opt == "4":
        # Follower Farm
        username = _loginInfo.username if _loginInfo.username != "" else input("%susername: %s" % (fg(207), attr(0)))
        password = _loginInfo.password if _loginInfo.password != "" else input("%spassword: %s" % (fg(207), attr(0)))
        target = input("%sTarget account name: %s" % (fg(207), attr(0)))
        total = int(input("%sTotal Follow: %s" % (fg(10), attr(0))))
        res = Instagram.login(username, password)
        userExist = Instagram.navigateTo(target, "followers")
        if res & userExist:
            Instagram.getFollowings(total)
            Instagram.userAction("Follow")
            Instagram.message()
            Instagram.closeBot()
        else:
            Instagram.closeBot()
    elif opt == "5":
        # Unfollow Farm
        username = _loginInfo.username if _loginInfo.username != "" else input("%susername: %s" % (fg(207), attr(0)))
        password = _loginInfo.password if _loginInfo.password != "" else input("%spassword: %s" % (fg(207), attr(0)))
        total = int(input("%sTotal unFollow: %s" % (fg(10), attr(0))))
        res = Instagram.login(username, password)
        userExist = Instagram.navigateTo(username, "following")
        if res & userExist:
            Instagram.getFollowings(total)
            Instagram.userAction("unFollow")
            Instagram.message()
            Instagram.closeBot()
        else:
            Instagram.closeBot()
    elif opt == "8":
        # Remove Requests
        os.system("cls")
        username = _loginInfo.username if _loginInfo.username != "" else input("%susername: %s" % (fg(207), attr(0)))
        password = _loginInfo.password if _loginInfo.password != "" else input("%spassword: %s" % (fg(207), attr(0)))
        res = Instagram.login(username, password)
        if res:
            Instagram.removeRequests()
            Instagram.message()
            Instagram.closeBot()
        else:
            Instagram.closeBot()
