from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from colored import fg, attr
import urllib.request
from PIL import Image
import requests

import warnings
import time
import os
import json

import _loginInfo
import _scripts

warnings.filterwarnings("ignore", category=DeprecationWarning)

class Instagram:
    def __init__(self):
        # Paths
        self.driverPath = "./driver/chromedriver.exe"
        self.imageFolderPath = "./images"
        self.requestedAccountsFilePath = "data/pending_follow_requests.json"
        # Chrome Options
        self.service = Service(self.driverPath)
        self.chromeOpt = webdriver.ChromeOptions()
        self.chromeOpt.add_argument("--lang=en")
        self.chromeOpt.add_argument("--log-level=3")
        self.chromeOpt.add_argument("--headless")
        self.chromeOpt.add_argument("window-size=1920,1080")
        self.chromeOpt.add_argument("window-position=0,0")
        self.chromeOpt.add_argument("--start-maximized")
        self.chromeOpt.add_argument("--force-dark-mode")
        self.chromeOpt.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
        self.chromeOpt.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": "2"})
        self.chromeOpt.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.browser = webdriver.Chrome(service=self.service, options=self.chromeOpt)
        # Variables
        self.userList = []
        self.pendingFollowRequests = []
        self.followTimeout = 45
        self.UnfollowTimeout = 30

    def messages(self):
        return {
            "login": "%s\n >>> Logging in...%s" % (fg(1), attr(0)),
            "imgNotFound": "%s\n >>> Image not found!%s" % (fg(1), attr(0)),
            "imgDeleted": "%s\n >>> Image deleted!%s" % (fg(2), attr(0)),
            "allImgDeleted": "%s\n >>> All images deleted!%s" % (fg(2), attr(0)),
            "downloading": "%s\n >>> Downloading image...%s" % (fg(2), attr(0)),
            "downloaded": "%s\n >>> Image downloaded!%s" % (fg(2), attr(0)),
            "freeze": "%s\n >>> Freezing account...%s" % (fg(2), attr(0)),
            "freezeResult": "%s\n >>> Results loading...%s" % (fg(2), attr(0)),
            "countFollowers": "%s\n >>> Counting followers...%s" % (fg(2), attr(0)),
            "savingFollowers": "%s\n >>> Saving followers...%s" % (fg(2), attr(0)),
            "getFollowersSuccess": "%s\n >>> Followers successfully saved to 'followers.txt' file!%s" % (fg(2), attr(0)),
            "getFollowersError": "%s\n >>> Something went wrong while saving followers. Please try again later.%s" % (fg(1), attr(0)),
            "importingRequests": "%s\n >>> Importing data from 'pending_follow_requests.json' file...%s" % (fg(2), attr(0)),
            "importingRequestsError": "%s\n >>> Something went wrong while importing data from 'pending_follow_requests.json' file. Please make sure the file exists and meets the requirements. Read the README.md file for more information.%s" % (fg(1), attr(0)),
            "removeRequest": "%s\n >>> Removing requests...%s" % (fg(2), attr(0)),
            "rewritingRequests": "%s\n >>> Re-writing 'pending_follow_requests.json' file...%s" % (fg(2), attr(0)),
            "done": "%s\n >>> DONE!%s" % (fg(2), attr(0)),
        }

    def createImagePath(self):
        if not os.path.exists(self.imageFolderPath):
            os.makedirs(self.imageFolderPath)

    def clearc(self):
        os.system("cls")

    def getTotalFileSum(self, path):
        total = 0
        for _, _, files in os.walk(path):
            total += len(files)

        if total == 0:
            return 1
        else:
            return total + 1

    def login(self, username, password):
        self.clearc()
        print(self.messages()["login"])
        time.sleep(2)

        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)

        self.browser.find_element(By.NAME, "username").send_keys(username)
        self.browser.find_element(By.NAME, "password").send_keys(password)
        self.browser.find_element(By.XPATH, '//*[@type="submit"]').click()
        time.sleep(7)

        try:
            isPasswordIncorrect = self.browser.find_element(
                By.XPATH, '//*[@id="loginForm"]/span/div'
            )
            if isPasswordIncorrect:
                print(f"%s>>> {isPasswordIncorrect.text} %s" % (fg(1), attr(0)))
                return False
        except:
            pass

        try:
            errmsg = self.browser.find_element(By.XPATH, '//*[@id="slfErrorAlert"]')
            print(f"%s>>> {errmsg.text} \n%s" % (fg(1), attr(0)))
            return False
        except:
            return True

    def closeBot(self):
        self.browser.quit()

    def resetBot(self):
        self.userList = []
        self.pendingFollowRequests = []

    def showImg(self):
        self.clearc()

        fileName = input("\n%s[post / pp / result] :%s" % (fg(30), attr(0)))
        try:
            img = Image.open(f"{self.imageFolderPath}/{fileName}.png")
            img.show()
        except FileNotFoundError:
            print(self.messages()["fileNotFound"])

    def deleteImg(self):
        self.clearc()

        files = ["pp", "post", "result"]
        fileName = input(f"\n%s {files}: %s" % (fg(30), attr(0)))

        if fileName == "all":
            for file in files:
                try:
                    os.remove(f"{self.imageFolderPath}/{file}.png")
                except FileNotFoundError:
                    pass
            print(self.messages()["allImgDeleted"])
        else:
            try:
                os.remove(f"{self.imageFolderPath}/{fileName}.png")
                print(self.messages()["imgDeleted"])
            except FileNotFoundError:
                pass

    def downloadPP(self, username):
        self.clearc()
        self.messages()["downloading"]

        url = f"https://www.instagram.com/{username}/?__a=1&__d=1"
        pic = requests.get(url).json()["graphql"]["user"]["profile_pic_url_hd"]

        # create images folder if not exists
        self.createImagePath()
        fileNum = self.getTotalFileSum(self.imageFolderPath)

        urllib.request.urlretrieve(pic, f"{self.imageFolderPath}/pp{fileNum}.png")

        print(self.messages()["downloaded"])

    def downloadPost(self, link=""):
        self.clearc()
        self.messages()["downloading"]

        # if link is not a post link, convert it to post link
        postId = link.split("/")[-2]

        self.browser.get(f"https://www.instagram.com/p/{postId}/media/?size=l")
        time.sleep(2)

        src = self.browser.find_element(By.TAG_NAME, "img").get_attribute("src")

        # create images folder if not exists
        self.createImagePath()
        fileNum = self.getTotalFileSum(self.imageFolderPath)

        urllib.request.urlretrieve(src, f"{self.imageFolderPath}/post{fileNum}.png")

        print(self.messages()["downloaded"])

    def freezeAccount(self, password):
        self.clearc()
        print(self.messages()["freeze"])

        self.browser.get("https://www.instagram.com/accounts/remove/request/temporary/")
        time.sleep(2)
        self.browser.find_element(By.XPATH, '//*[@id="deletion-reason"]').click()
        time.sleep(2)
        self.browser.find_element(By.XPATH, "//option[@value='need-break']").click()
        self.browser.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
        time.sleep(2)
        self.browser.find_element(By.CSS_SELECTOR, "article form button").click()
        time.sleep(2)
        self.browser.find_element(By.CSS_SELECTOR, "article form div div button").click()

        print(self.messages()["freezeResult"])
        time.sleep(2)

        self.browser.save_screenshot(f"{self.imageFolderPath}/result.png")
        img = Image.open(f"{self.imageFolderPath}/result.png")
        time.sleep(2)

        img.show()

    def checkPageLoadBlock(self, action):
        isBlocked = False
        
        try:
            time.sleep(1)
            isBlocked = self.browser.find_element(By.XPATH, "//*[@aria-label='Error']")
            if isBlocked.is_displayed(): 
                print( f"%s\n >>> Instagram blocked {action}. Try again later. %s" % (fg(1), attr(0)))
                self.resetBot()
        except:
            pass

        return isBlocked

    def navigateTo(self, user, path):
        self.browser.get(f"https://www.instagram.com/{user}")
        print(f"%s >>> Navigating to {path}\n%s" % (fg(61), attr(0)))
        time.sleep(3)

        if self.checkPageLoadBlock("page loads"):
            return False

        try:
            self.browser.find_element(By.XPATH, f'//*[@href="/{user}/{path}/"]').click()
            time.sleep(2)
            return True
        except:
            print(f"%s >>> {user} does not exist!%s" % (fg(1), attr(0)))
            return False

    def userAction(self, action):
        count = 0
        hrefs = (
            action == "removeRequest" and self.pendingFollowRequests or self.userList
        )

        for user in hrefs:
            self.clearc()

            skip = True

            print(f"%s >>> Total {action}ed: {count}/{len(hrefs)} %s" % (fg(43), attr(0)))
            self.browser.get(
                action == "removeRequest"
                and user["string_list_data"][0]["href"]
                or user
            )

            if self.checkPageLoadBlock(f"{action} actions"):
                return False

            # Execute follow/unfollow aciton
            try:
                time.sleep(2)

                if action == "Follow":
                    ################################
                    ############ Follow ############
                    ################################

                    # This will skip ["Requested", "Following", "Follow Back"] buttons
                    try:
                        followButton = self.browser.find_element(
                            By.XPATH,
                            "//header//*[@type='button']//*[contains(text(), 'Follow')]",
                        )
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
                        popupButton = self.browser.find_element(
                            By.XPATH,
                            "//header//*[@type='button']//*[contains(text(), 'Requested')]",
                        )
                        if popupButton.text == "Requested":
                            if popupButton.text == "Requested":
                                popupButton.click()
                                skip = False
                    except:
                        pass

                    # Click unfollow button in popup dialog
                    time.sleep(1.5)
                    try:
                        unFollowButton = self.browser.find_element(
                            By.XPATH, "//*/button[contains(text(), 'Unfollow')]"
                        )
                        if unFollowButton.text == "Unfollow":
                            unFollowButton.click()
                            skip = False
                    except:
                        pass

                    self.reWritePendingRequests(user)
                else:
                    ################################
                    ########### unFollow ###########
                    ################################

                    # Open popup dialog
                    try:
                        popupButton = self.browser.find_element(
                            By.XPATH,
                            "//header//*[@type='button']//*[contains(text(), 'Following')]",
                        )
                        if popupButton.text == "Following":
                            if popupButton.text == "Following":
                                popupButton.click()
                                skip = False
                    except:
                        pass

                    time.sleep(1.5)

                    try:
                        unFollowButton = self.browser.find_element(
                            By.XPATH,
                            "//*/div[@role='button']//*[contains(text(), 'Unfollow')]",
                        )
                        if unFollowButton.text == "Unfollow":
                            unFollowButton.click()
                            skip = False
                    except:
                        pass
            except Exception as e:
                print(f"%s >>> Something went wrong on {action} action. Skipping...%s" % (fg(1), attr(0)))
                print(e)

            # Check action block
            try:
                time.sleep(1.5)
                self.browser.find_element(By.TAG_NAME, "h3")
                print(
                    f"%s\n >>> Instagram blocked {action} actions. Try again later. %s"
                    % (fg(1), attr(0))
                )
                break
            except:
                pass

            count += 1

            # Wait for 25 seconds to avoid Instagram blocking actions. You can increase the time if you get blocked so often.
            # Please note that the more you increase the time, the more time it will take to finish the process.
            if skip:
                print(
                    f"%s\n >>> Skipping {action} action cause it's already done. %s"
                    % (fg(1), attr(0))
                )
                time.sleep(1)
            else:
                sleepTime = (
                    action == "Follow" and self.followTimeout or self.UnfollowTimeout
                )
                for wait in range(sleepTime):
                    print(
                        f"%s >>> {sleepTime-wait} seconds left to {action.lower()} next user... %s"
                        % (fg(2), attr(0)),
                        end="\r",
                    )
                    time.sleep(1)

    def getFollowings(self, total):
        time.sleep(5)

        while True:
            self.browser.execute_script(_scripts.scrollScript)
            time.sleep(2)

            newCount = len(
                self.browser.find_elements(By.XPATH, "//*[@class='_aano']/div/div/div")
            )
            self.clearc()

            print(f"%s >>> Total Collected User Count: {newCount}/{total} %s" % (fg(10), attr(0)))

            if newCount <= 1:
                break

            if newCount < total:
                time.sleep(0.5)
            else:
                break

        followers = self.browser.find_elements(
            By.XPATH, "//*[@class='_aano']/div/div/div"
        )
        self.userList = []

        i = 0
        for user in followers:
            link = user.find_element(By.TAG_NAME, "a").get_attribute("href")
            self.userList.append(link)
            i += 1
            if i >= total:
                break

    def getFollowers(self, username):
        os.system("cls")
        self.browser.get(f"https://www.instagram.com/{username}/followers")
        time.sleep(3)

        self.messages()["countFollowers"]

        counterFollowers = len(
            self.browser.find_elements(By.XPATH, "//*[@class='_aano']/div/div/div")
        )
        print(f" >>> Started to Counting Followers: {counterFollowers}")

        while True:
            self.browser.execute_script(_scripts.scrollScript)
            time.sleep(2)

            newCount = len(
                self.browser.find_elements(By.XPATH, "//*[@class='_aano']/div/div/div")
            )
            self.clearc()

            if counterFollowers != newCount:
                counterFollowers = newCount
                os.system("cls")
                print(f"%s >>> Collected Followers: {newCount}%s" % (fg(10), attr(0)))
            else:
                break

        self.messages()["savingFollowers"]

        try:
            totalFollowers = self.browser.find_elements(
                By.XPATH, "//*[@class='_aano']/div/div/div"
            )

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
            print(self.messages()["getFollowersError"])

        print(self.messages()["getFollowersSuccess"])

    def removeRequests(self):
        os.system("cls")
        print(self.messages()["importingRequests"])

        # Importing data from 'pending_follow_requests.json' file
        try:
            f = open(self.requestedAccountsFilePath)
            data = json.load(f)
            for user in data["relationships_follow_requests_sent"]:
                self.pendingFollowRequests.append(user)
            f.close()
        except:
            print(self.messages()["importingRequestsError"])
            return

        print(self.messages()["removeRequest"])
        self.userAction("removeRequest")

    def reWritePendingRequests(self, user):
        print(self.messages()["rewritingRequests"])

        # deleting user from 'pending_follow_requests.json' file
        with open(self.requestedAccountsFilePath, "r", encoding="utf-8") as file:
            data = json.load(file)
            for i in range(len(data["relationships_follow_requests_sent"])):
                if (
                    data["relationships_follow_requests_sent"][i]["string_list_data"][
                        0
                    ]["href"]
                    == user["string_list_data"][0]["href"]
                ):
                    del data["relationships_follow_requests_sent"][i]
                    break

        # re-writing 'pending_follow_requests.json' file
        newFile = {
            "relationships_follow_requests_sent": data[
                "relationships_follow_requests_sent"
            ]
        }
        with open(self.requestedAccountsFilePath, "w", encoding="utf-8") as file:
            json.dump(newFile, file, indent=3)

if __name__ == "__main__":
    Instagram = Instagram()

    try:
        while True:
            print("%s\n\n∴∵∴∵∴∵ INSTAGRAM TOOL ∴∵∴∵∴∵∴\n%s" % (fg(171), attr(0)))
            opt = input(
                "%s"
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
                ">>> ENTER NUMBER: %s"
                "" % (fg(171), attr(0))
            )

            if opt == "0":
            # DOWNLOAD PROFILE PICTURE #
                username = input("%susername: %s" % (fg(207), attr(0)))
                Instagram.downloadPP(username)
                Instagram.resetBot()
            elif opt == "9":
                Instagram.closeBot()
                exit()
            elif opt == "1":
            # DOWNLOAD POST #
                link = input("%sPost Link: %s" % (fg(207), attr(0)))
                Instagram.downloadPost(link)
                Instagram.resetBot()
            elif opt == "2":
            # FREEZE ACCOUNT #
                username = (
                    _loginInfo.username
                    if _loginInfo.username != None
                    else input("%susername: %s" % (fg(207), attr(0)))
                )
                password = (
                    _loginInfo.password
                    if _loginInfo.password != None
                    else input("%spassword: %s" % (fg(207), attr(0)))
                )
                res = Instagram.login(username, password)
                if res:
                    Instagram.freezeAccount(password)
                    Instagram.resetBot()
                else:
                    Instagram.resetBot()
            elif opt == "6":
            # OPEN SELECTED PICTURE #
                Instagram.showImg()
            elif opt == "7":
            # DELETE SELECTED PICTURE #
                Instagram.deleteImg()
            elif opt == "3":
            # GET FOLLOWERS #
                username = (
                    _loginInfo.username
                    if _loginInfo.username != None
                    else input("%susername: %s" % (fg(207), attr(0)))
                )
                password = (
                    _loginInfo.password
                    if _loginInfo.password != None
                    else input("%spassword: %s" % (fg(207), attr(0)))
                )
                res = Instagram.login(username, password)
                if res:
                    Instagram.getFollowers(username)
                    Instagram.resetBot()
                else:
                    Instagram.resetBot()
            elif opt == "4":
                print(_loginInfo.username)
            # FOLLOW FARM #
                username = (
                    _loginInfo.username
                    if _loginInfo.username != None
                    else input("%susername: %s" % (fg(207), attr(0)))
                )
                password = (
                    _loginInfo.password
                    if _loginInfo.password != None
                    else input("%spassword: %s" % (fg(207), attr(0)))
                )
                target = input("%sTarget account name: %s" % (fg(207), attr(0)))
                total = int(input("%sTotal Follow: %s" % (fg(10), attr(0))))
                res = Instagram.login(username, password)
                userExist = Instagram.navigateTo(target, "followers")
                if res & userExist:
                    Instagram.getFollowings(total)
                    Instagram.userAction("Follow")
                    print(Instagram.messages()["done"])
                    Instagram.resetBot()
                else:
                    Instagram.resetBot()
            elif opt == "5":
            # UNFOLLOW FARM #
                username = (
                    _loginInfo.username
                    if _loginInfo.username != None
                    else input("%susername: %s" % (fg(207), attr(0)))
                )
                password = (
                    _loginInfo.password
                    if _loginInfo.password != None
                    else input("%spassword: %s" % (fg(207), attr(0)))
                )
                total = int(input("%sTotal unFollow: %s" % (fg(10), attr(0))))
                res = Instagram.login(username, password)
                userExist = Instagram.navigateTo(username, "following")
                if res & userExist:
                    Instagram.getFollowings(total)
                    Instagram.userAction("unFollow")
                    print(Instagram.messages()["done"])
                    Instagram.resetBot()
                else:
                    Instagram.resetBot()
            elif opt == "8":
            # REMOVE REQUESTS #
                username = (
                    _loginInfo.username
                    if _loginInfo.username != None
                    else input("%susername: %s" % (fg(207), attr(0)))
                )
                password = (
                    _loginInfo.password
                    if _loginInfo.password != None
                    else input("%spassword: %s" % (fg(207), attr(0)))
                )
                res = Instagram.login(username, password)
                if res:
                    Instagram.removeRequests()
                    print(Instagram.messages()["done"])
                    Instagram.resetBot()
                else:
                    Instagram.resetBot()
    except e as Exception:
        print(f"%s >>> Shutting down... %s" % (fg(10), attr(0)))
    finally:
        Instagram.closeBot()
        exit()