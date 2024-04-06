import warnings
import time
import os
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from colored import fg, attr
import urllib.request
from PIL import Image
import requests

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
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--lang=en")
        self.chrome_options.add_argument("--log-level=3")

        # The headless option may lead to blocks from Instagram if used too often. 
        # You might want to disable it in your use case.
        self.chrome_options.add_argument("--headless")
        
        self.chrome_options.add_argument("window-size=1920,1080")
        self.chrome_options.add_argument("window-position=0,0")
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--force-dark-mode")
        self.chrome_options.add_experimental_option(
            "excludeSwitches", ["disable-popup-blocking"]
        )
        self.chrome_options.add_experimental_option(
            "prefs", {"profile.default_content_setting_values.notifications": "2"}
        )
        self.chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-logging"]
        )
        self.browser = webdriver.Chrome(
            service=self.service, options=self.chrome_options
        )

        # Variables
        self.user_list = []
        self.pendingFollowRequests = []
        self.followTimeout = 20
        self.unfollow_timeout = 10
        self.isLoggedIn = False

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
            "getFollowersSuccess": "%s\n >>> Followers successfully saved to 'followers.txt' file!%s"
            % (fg(2), attr(0)),
            "getFollowersError": "%s\n >>> Something went wrong while saving followers. Please try again later.%s"
            % (fg(1), attr(0)),
            "importingRequests": "%s\n >>> Importing data from 'pending_follow_requests.json' file...%s"
            % (fg(2), attr(0)),
            "importingRequestsError": (
                "%s\n >>> Something went wrong while importing data from "
                "'pending_follow_requests.json' file. Please make sure the file exists "
                "and meets the requirements. Read the README.md file for more information.%s"
            )
            % (fg(1), attr(0)),
            "removeRequest": "%s\n >>> Removing requests...%s" % (fg(2), attr(0)),
            "rewritingRequests": "%s\n >>> Re-writing 'pending_follow_requests.json' file...%s"
            % (fg(2), attr(0)),
            "done": "%s\n >>> DONE!%s" % (fg(2), attr(0)),
        }

    def create_image_path(self):
        if not os.path.exists(self.imageFolderPath):
            os.makedirs(self.imageFolderPath)

    def clearc(self):
        os.system("cls")

    def get_total_file_sum(self, path):
        total = 0
        for _, _, files in os.walk(path):
            total += len(files)

        if total == 0:
            return 1
        else:
            return total + 1

    def login(self, username, password):
        if self.isLoggedIn:
            return True

        self.clearc()
        print(self.messages()["login"])
        time.sleep(2)

        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(7)

        self.browser.find_element(By.NAME, "username").send_keys(username)
        self.browser.find_element(By.NAME, "password").send_keys(password)
        time.sleep(1)
        self.browser.find_element(By.XPATH, '//*[@type="submit"]').click()
        time.sleep(10)

        try:
            isPasswordIncorrect = self.browser.find_element(
                By.XPATH, '//*[@id="loginForm"]/span/div'
            )
            if isPasswordIncorrect:
                print(f"%s>>> {isPasswordIncorrect.text} %s" % (fg(1), attr(0)))
                return False
        except NoSuchElementException:
            pass

        try:
            errmsg = self.browser.find_element(By.XPATH, '//*[@id="slfErrorAlert"]')
            print(f"%s>>> {errmsg.text} \n%s" % (fg(1), attr(0)))
            return False
        except NoSuchElementException:
            self.isLoggedIn = True
            return True

    def close_bot(self):
        self.browser.quit()

    def reset_bot(self):
        self.user_list = []
        self.pendingFollowRequests = []

    def show_img(self):
        self.clearc()

        fileName = input("\n%s[post / pp / result] :%s" % (fg(30), attr(0)))
        try:
            img = Image.open(f"{self.imageFolderPath}/{fileName}.png")
            img.show()
        except FileNotFoundError:
            print(self.messages()["fileNotFound"])

    def delete_img(self):
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

    def download_pp(self, username):
        self.clearc()
        self.messages()["downloading"]

        url = f"https://www.instagram.com/{username}/?__a=1&__d=1"
        pic = requests.get(url).json()["graphql"]["user"]["profile_pic_url_hd"]

        # create images folder if not exists
        self.create_image_path()
        fileNum = self.get_total_file_sum(self.imageFolderPath)

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
        self.create_image_path()
        fileNum = self.get_total_file_sum(self.imageFolderPath)

        urllib.request.urlretrieve(src, f"{self.imageFolderPath}/post{fileNum}.png")

        print(self.messages()["downloaded"])

    def freeze_account(self, password):
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
        self.browser.find_element(
            By.CSS_SELECTOR, "article form div div button"
        ).click()

        print(self.messages()["freezeResult"])
        time.sleep(2)

        self.browser.save_screenshot(f"{self.imageFolderPath}/result.png")
        img = Image.open(f"{self.imageFolderPath}/result.png")
        time.sleep(2)

        img.show()

    def check_page_load_block(self, action):
        blocked = False

        try:
            time.sleep(1)
            blocked = self.browser.find_element(By.XPATH, "//*[@aria-label='Error']")
            if blocked.is_displayed():
                print(
                    f"%s\n >>> Instagram blocked {action}. Try again later. %s"
                    % (fg(1), attr(0))
                )
                self.reset_bot()
        except NoSuchElementException:
            pass

        return blocked

    def check_popup_block(self, action):
        blocked = False

        try:
            time.sleep(1.5)

            errText = self.browser.find_element(
                By.XPATH, "//*[@role='dialog']//span[1]"
            ).text

            if errText == "Try Again Later":
                blocked = True
                print(
                    f"%s\n >>> Instagram blocked {action}. Try again later. %s"
                    % (fg(1), attr(0))
                )
                self.reset_bot()
        except NoSuchElementException:
            pass

        return blocked

    def navigate_to(self, user, path):
        self.browser.get(f"https://www.instagram.com/{user}")
        print(f"%s >>> Navigating to {path}\n%s" % (fg(61), attr(0)))
        time.sleep(3)

        if self.check_page_load_block("page loads"):
            return False

        try:
            self.browser.find_element(By.XPATH, f'//*[@href="/{user}/{path}/"]').click()
            time.sleep(2)
            return True
        except NoSuchElementException:
            print(f"%s >>> {user} does not exist!%s" % (fg(1), attr(0)))
            return False

    def userAction(self, action):
        count = 0
        hrefs = (
            action == "removeRequest" and self.pendingFollowRequests or self.user_list
        )

        for user in hrefs:
            self.clearc()

            skip = True

            print(
                f"%s >>> Total {action}ed: {count}/{len(hrefs)} %s" % (fg(43), attr(0))
            )
            self.browser.get(
                action == "removeRequest"
                and user["string_list_data"][0]["href"]
                or user
            )

            if self.check_page_load_block(f"{action} actions"):
                return False

            # Execute follow/unfollow aciton
            try:
                time.sleep(2)

                # Follow
                if action == "Follow":
                    # This will skip ["Requested", "Following", "Follow Back"] buttons
                    try:
                        followButton = self.browser.find_element(
                            By.XPATH,
                            "//header//*[@type='button']//*[contains(text(), 'Follow')]",
                        )
                        if followButton.text == "Follow":
                            followButton.click()
                            skip = False
                    except NoSuchElementException:
                        pass

                # removeRequest
                elif action == "removeRequest":
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
                    except NoSuchElementException:
                        pass

                    # Click unfollow button in popup dialog
                    time.sleep(1.5)
                    try:
                        unfollow_button = self.browser.find_element(
                            By.XPATH, "//*/button[contains(text(), 'Unfollow')]"
                        )
                        if unfollow_button.text == "Unfollow":
                            unfollow_button.click()
                            skip = False
                    except NoSuchElementException:
                        pass

                    self.re_write_pending_requests(user)

                # unFollow
                else:
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
                    except NoSuchElementException:
                        pass

                    time.sleep(1.5)

                    try:
                        unfollow_button = self.browser.find_element(
                            By.XPATH,
                            "//*/div[@role='button']//*[contains(text(), 'Unfollow')]",
                        )
                        if unfollow_button.text == "Unfollow":
                            unfollow_button.click()
                            skip = False
                    except NoSuchElementException:
                        pass
            except Exception as e:
                print(
                    f"%s >>> Something went wrong on {action} action. Skipping...%s"
                    % (fg(1), attr(0))
                )
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
            except NoSuchElementException:
                pass

            # Check popup block
            if self.check_popup_block(action):
                return False

            count += 1

            # Wait for 25 seconds to avoid Instagram blocking actions.
            # You can increase the time if you get blocked so often.
            # Please note that the more you increase the time,
            # the more time it will take to finish the process.
            if skip:
                print(
                    f"%s\n >>> Skipping {action} action cause it's already done. %s"
                    % (fg(1), attr(0))
                )
                time.sleep(1)
            else:
                sleepTime = (
                    action == "Follow" and self.followTimeout or self.unfollow_timeout
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

            new_count = len(
                self.browser.find_elements(By.XPATH, "//*[@class='_aano']/div/div/div")
            )
            self.clearc()

            print(
                f"%s >>> Total Collected User Count: {new_count}/{total} %s"
                % (fg(10), attr(0))
            )

            if new_count <= 1:
                break

            if new_count < total:
                time.sleep(0.5)
            else:
                break

        followers = self.browser.find_elements(
            By.XPATH, "//*[@class='_aano']/div/div/div"
        )
        self.user_list = []

        i = 0
        for user in followers:
            link = user.find_element(By.TAG_NAME, "a").get_attribute("href")
            self.user_list.append(link)
            i += 1
            if i >= total:
                break

    def get_followers(self, username):
        os.system("cls")
        self.browser.get(f"https://www.instagram.com/{username}/followers")
        time.sleep(3)

        self.messages()["countFollowers"]

        followers_count = len(
            self.browser.find_elements(By.XPATH, "//*[@class='_aano']/div/div/div")
        )
        print(f" >>> Started to Counting Followers: {followers_count}")

        while True:
            self.browser.execute_script(_scripts.scrollScript)
            time.sleep(2)

            new_count = len(
                self.browser.find_elements(By.XPATH, "//*[@class='_aano']/div/div/div")
            )
            self.clearc()

            if followers_count is not new_count:
                followers_count = new_count
                os.system("cls")
                print(f"%s >>> Collected Followers: {new_count}%s" % (fg(10), attr(0)))
            else:
                break

        self.messages()["savingFollowers"]

        try:
            total_followers = self.browser.find_elements(
                By.XPATH, "//*[@class='_aano']/div/div/div"
            )

            Flist = []
            i = 0
            for users in total_followers:
                i += 1
                if i == followers_count:
                    break

                link = users.find_element(By.TAG_NAME, "a").get_attribute("href")
                Flist.append(link)
                with open("followers.txt", "w", encoding="utf-8") as file:
                    for item in Flist:
                        file.write(item + "\n")
        except NoSuchElementException:
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
        except NoSuchElementException:
            print(self.messages()["importingRequestsError"])
            return

        print(self.messages()["removeRequest"])
        self.userAction("removeRequest")

    def re_write_pending_requests(self, user):
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


Instagram = Instagram()

if __name__ == "__main__":
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
                Instagram.download_pp(username)
                Instagram.reset_bot()
            elif opt == "9":
                Instagram.close_bot()
                exit()
            elif opt == "1":
                # DOWNLOAD POST #
                link = input("%sPost Link: %s" % (fg(207), attr(0)))
                Instagram.downloadPost(link)
                Instagram.reset_bot()
            elif opt == "2":
                # FREEZE ACCOUNT #
                username = (
                    _loginInfo.username
                    if _loginInfo.username is not None
                    else input("%susername: %s" % (fg(207), attr(0)))
                )
                password = (
                    _loginInfo.password
                    if _loginInfo.password is not None
                    else input("%spassword: %s" % (fg(207), attr(0)))
                )
                LOGGED = Instagram.login(username, password)
                if LOGGED:
                    Instagram.freeze_account(password)
                    Instagram.reset_bot()
                else:
                    Instagram.reset_bot()
            elif opt == "6":
                # OPEN SELECTED PICTURE #
                Instagram.show_img()
            elif opt == "7":
                # DELETE SELECTED PICTURE #
                Instagram.delete_img()
            elif opt == "3":
                # GET FOLLOWERS #
                username = (
                    _loginInfo.username
                    if _loginInfo.username is not None
                    else input("%susername: %s" % (fg(207), attr(0)))
                )
                password = (
                    _loginInfo.password
                    if _loginInfo.password is not None
                    else input("%spassword: %s" % (fg(207), attr(0)))
                )
                LOGGED = Instagram.login(username, password)
                if LOGGED:
                    Instagram.get_followers(username)
                    Instagram.reset_bot()
                else:
                    Instagram.reset_bot()
            elif opt == "4":
                # FOLLOW FARM #
                username = (
                    _loginInfo.username
                    if _loginInfo.username is not None
                    else input("%susername: %s" % (fg(207), attr(0)))
                )
                password = (
                    _loginInfo.password
                    if _loginInfo.password is not None
                    else input("%spassword: %s" % (fg(207), attr(0)))
                )
                target = input("%sTarget account name: %s" % (fg(207), attr(0)))
                total = int(input("%sTotal Follow: %s" % (fg(10), attr(0))))
                LOGGED = Instagram.login(username, password)
                USER_EXIST = Instagram.navigate_to(target, "followers")
                if LOGGED & USER_EXIST:
                    Instagram.getFollowings(total)
                    Instagram.userAction("Follow")
                    print(Instagram.messages()["done"])
                    Instagram.reset_bot()
                else:
                    Instagram.reset_bot()
            elif opt == "5":
                # UNFOLLOW FARM #
                username = (
                    _loginInfo.username
                    if _loginInfo.username is not None
                    else input("%susername: %s" % (fg(207), attr(0)))
                )
                password = (
                    _loginInfo.password
                    if _loginInfo.password is not None
                    else input("%spassword: %s" % (fg(207), attr(0)))
                )
                total = int(input("%sTotal unFollow: %s" % (fg(10), attr(0))))
                LOGGED = Instagram.login(username, password)
                USER_EXIST = Instagram.navigate_to(username, "following")
                if LOGGED & USER_EXIST:
                    Instagram.getFollowings(total)
                    Instagram.userAction("unFollow")
                    print(Instagram.messages()["done"])
                    Instagram.reset_bot()
                else:
                    Instagram.reset_bot()
            elif opt == "8":
                # REMOVE REQUESTS #
                username = (
                    _loginInfo.username
                    if _loginInfo.username is not None
                    else input("%susername: %s" % (fg(207), attr(0)))
                )
                password = (
                    _loginInfo.password
                    if _loginInfo.password is not None
                    else input("%spassword: %s" % (fg(207), attr(0)))
                )
                LOGGED = Instagram.login(username, password)
                if LOGGED:
                    Instagram.removeRequests()
                    print(Instagram.messages()["done"])
                    Instagram.reset_bot()
                else:
                    Instagram.reset_bot()
    except KeyboardInterrupt:
        print("%s >>> Shutting down... %s" % (fg(10), attr(0)))
    except Exception as e:
        print("Caught an unexpected error: %s" % e)
        print("%s >>> Shutting down... %s" % (fg(10), attr(0)))
    finally:
        Instagram.close_bot()
        exit()
