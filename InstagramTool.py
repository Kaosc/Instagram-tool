import warnings
import time
import os
import json
import random
import math

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from colored import fg, attr
import urllib.request
from PIL import Image
import instaloader

import _loginInfo
import _scripts
import _excludedUsers

warnings.filterwarnings("ignore", category=DeprecationWarning)


class InstagramTool:
    def __init__(self):
        # Paths
        self.driverPath = "./driver/chromedriver.exe"
        self.imageFolderPath = "./images"
        self.requestedAccountsFilePath = "data/pending_follow_requests.json"

        # Chrome driver setup
        self.service = Service(self.driverPath)
        self.chrome_options = webdriver.ChromeOptions()

        # Chrome options

        # The headless option may lead you to get blocked by Instagram if used too often.
        # You might want to disable it in your use case.
        # Recommended to use it without headless mode.
        self.chrome_options.add_argument("--headless")

        self.chrome_options.add_argument("--lang=en")
        self.chrome_options.add_argument("--log-level=3")
        self.chrome_options.add_argument("window-size=1920,1080")
        self.chrome_options.add_argument("window-position=0,0")
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--force-dark-mode")
        self.chrome_options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
        self.chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": "2"})
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.92 Safari/537.36")
        self.browser = webdriver.Chrome(service=self.service, options=self.chrome_options)

        # Variables
        self.user_list = []
        self.pendingFollowRequests = []
        self.isLoggedIn = False

        # Login info
        self.username = None
        self.password = None

    def messages(self):
        return {
            "login": "%s\n>>> Logging in...%s" % (fg(1), attr(0)),
            "imgNotFound": "%s\n>>> Image not found!%s" % (fg(1), attr(0)),
            "imgDeleted": "%s\n>>> Image deleted!%s" % (fg(2), attr(0)),
            "allImgDeleted": "%s\n>>> All images deleted!%s" % (fg(2), attr(0)),
            "downloading": "%s\n>>> Downloading image...%s" % (fg(2), attr(0)),
            "downloaded": "%s\n>>> Image downloaded!%s" % (fg(2), attr(0)),
            "freeze": "%s\n>>> Freezing account...%s" % (fg(2), attr(0)),
            "freezeResult": "%s\n>>> Results loading...%s" % (fg(2), attr(0)),
            "countFollowers": "%s\n>>> Counting followers...%s" % (fg(2), attr(0)),
            "savingFollowers": "%s\n>>> Saving followers...%s" % (fg(2), attr(0)),
            "getFollowersSuccess": "%s\n>>> Followers successfully saved to 'followers.txt' file!%s" % (fg(2), attr(0)),
            "getFollowersError": "%s\n>>> Something went wrong while saving followers. Please try again later.%s" % (fg(1), attr(0)),
            "importingRequests": "%s\n>>> Importing data from 'pending_follow_requests.json' file...%s" % (fg(2), attr(0)),
            "importingRequestsError": (
                "%s\n>>> Something went wrong while importing data from 'pending_follow_requests.json' file. Please make sure the file exists and meets the requirements. Read the README.md file for more information.%s"
            )
            % (fg(1), attr(0)),
            "removeRequest": "%s\n>>> Removing requests...%s" % (fg(2), attr(0)),
            "rewritingRequests": "%s\n>>> Re-writing 'pending_follow_requests.json' file...%s" % (fg(2), attr(0)),
            "done": "%s\n>>> DONE!%s" % (fg(2), attr(0)),
            "followersNotAvailable": "%s>>> Followers not shown by account. Collecting available followers.%s" % (fg(2), attr(0)),
        }

    def clearc(self):
        os.system("cls")
        time.sleep(1)

    def close_bot(self):
        self.browser.quit()

    def reset_bot(self):
        self.user_list = []
        self.pendingFollowRequests = []

    def create_image_path(self):
        if not os.path.exists(self.imageFolderPath):
            os.makedirs(self.imageFolderPath)

    def get_total_file_sum(self, path):
        total = 0
        for _, _, files in os.walk(path):
            total += len(files)

        if total == 0:
            return 1
        else:
            return total + 1

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

    def login(self):
        if self.isLoggedIn:
            return True

        self.clearc()
        print(self.messages()["login"])
        time.sleep(2)

        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(7)

        self.browser.find_element(By.NAME, "username").send_keys(self.username)
        self.browser.find_element(By.NAME, "password").send_keys(self.password)
        time.sleep(1)
        self.browser.find_element(By.XPATH, '//*[@type="submit"]').click()
        time.sleep(10)

        # Check if password is incorrect
        try:
            isPasswordIncorrect = self.browser.find_element(By.XPATH, '//*[@id="loginForm"]/span/div')
            if isPasswordIncorrect:
                print(f"%s>>> {isPasswordIncorrect.text} %s" % (fg(1), attr(0)))
                return False
        except NoSuchElementException:
            pass

        # 2FA
        try:
            # Check if 2FA is required
            self.browser.find_element(By.XPATH, '//*[@aria-label="Two factor authentication lock icon"]')

            while True:
                try:
                    code = input("%s>>> Enter the 2FA code: %s" % (fg(207), attr(0)))

                    # Validate input
                    if not code.isdigit():
                        print("Invalid input. Please enter a numeric code.")
                        continue

                    # Clear the input field
                    self.browser.find_element(By.TAG_NAME, "input").send_keys(Keys.CONTROL + "a")
                    time.sleep(1)
                    self.browser.find_element(By.TAG_NAME, "input").send_keys(Keys.DELETE)
                    # Enter the code
                    self.browser.find_element(By.TAG_NAME, "input").send_keys(code)
                    time.sleep(1)
                    self.browser.find_element(By.XPATH, '//*[@type="button"]').click()
                    time.sleep(10)

                    try:
                        isCodeIncorrect = self.browser.find_element(By.XPATH, '//*[@id="twoFactorErrorAlert"]')
                    except NoSuchElementException:
                        isCodeIncorrect = False

                    if isCodeIncorrect:
                        print(f"%s>>> {isCodeIncorrect.text} %s" % (fg(1), attr(0)))
                    else:
                        break

                except ValueError:
                    print("Unexpected input format. Please try again.")
        except NoSuchElementException:
            pass

        time.sleep(6)

        # Check if login is successful
        try:
            errmsg = self.browser.find_element(By.XPATH, '//*[@id="slfErrorAlert"]')
            print(f"%s>>> {errmsg.text} \n%s" % (fg(1), attr(0)))
            return False
        except NoSuchElementException:
            self.isLoggedIn = True
            return True

    def download_pp(self, username):
        self.clearc()
        self.messages()["downloading"]

        path = f"{self.imageFolderPath}/{username}"

        loader = instaloader.Instaloader(save_metadata=False, quiet=True, dirname_pattern=path)

        try:
            loader.download_profile(username, profile_pic_only=True)

            id_file_path = os.path.join(path, f"{username}_id")
            if os.path.exists(id_file_path):
                os.remove(id_file_path)

            print(self.messages()["downloaded"])
        except Exception as e:
            print(f"An error occurred: {e}")

        # create images folder if not exists
        self.create_image_path()

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

    def check_page_load_block(self, action):
        blocked = False

        try:
            time.sleep(random.uniform(1, 2))
            blocked = self.browser.find_element(By.XPATH, "//*[@aria-label='Error']")
            if blocked.is_displayed():
                print(f"%s\n>>> Instagram blocked {action}. Try again later. %s" % (fg(1), attr(0)))
                self.reset_bot()
        except NoSuchElementException:
            pass

        return blocked

    def check_popup_block(self, action):
        blocked = False

        try:
            time.sleep(random.uniform(1.5, 2.5))

            errText = self.browser.find_element(By.XPATH, "//*[@role='dialog']//span[1]").text

            if errText == "Try Again Later":
                blocked = True
                print(f"%s\n>>> Instagram blocked {action}. Try again later. %s" % (fg(1), attr(0)))
                self.reset_bot()
        except NoSuchElementException:
            pass

        return blocked

    def navigate_to(self, user, path):
        self.browser.get(f"https://www.instagram.com/{user}")
        print(f"%s>>> Navigating to {path}\n%s" % (fg(61), attr(0)))
        time.sleep(random.uniform(2.5, 4.5))

        if self.check_page_load_block("page loads"):
            return False

        time.sleep(random.uniform(1.5, 2.5))

        try:
            self.browser.find_element(By.XPATH, f'//*[@href="/{user}/{path}/"]').click()
            time.sleep(random.uniform(2, 3))
            return True
        except NoSuchElementException:
            print(f"%s>>> {user} does not exist!%s" % (fg(1), attr(0)))
            return False

    def mimic_mouse(self):
        actions = ActionChains(self.browser)
        window_size = self.browser.get_window_size()
        width, height = window_size["width"], window_size["height"]

        for _ in range(2):
            try:
                x_offset = random.randint(0, int(math.floor(width - 1)))
                y_offset = random.randint(0, int(math.floor(height - 1)))
                actions.move_by_offset(x_offset, y_offset).perform()
            except Exception:
                pass

            time.sleep(random.uniform(0.5, 1.5))

    def mimic_goback(self):
        if random.randint(0, 4) == 1:
            self.browser.execute_script("window.history.go(-1)")
            time.sleep(random.uniform(2, 3))

    def userAction(self, action):
        count = 0
        hrefs = action == "removeRequest" and self.pendingFollowRequests or self.user_list

        # actions : instagram buttons text
        actions = {
            "Follow": "Follow",
            "unFollow": "Following",
            "removeRequest": "Requested",
        }

        for user in hrefs:
            self.clearc()

            # Skip excluded users for unfollow/follow action
            if action == "unFollow" or action == "Follow":
                if user.split("/")[-1] in _excludedUsers.EXCLUDED_USERNAMES:
                    print(f"%s>>> Skipping {user}... reason: excluded user %s" % (fg(1), attr(0)))
                    continue

            skip = True

            print(f"%s>>> Total {action}ed: {count}/{len(hrefs)} %s" % (fg(43), attr(0)))

            self.mimic_goback()

            self.browser.get(action == "removeRequest" and user["string_list_data"][0]["href"] or user)

            if self.check_page_load_block(f"{action} actions"):
                return False

            self.mimic_mouse()

            # Execute follow/unfollow aciton
            try:
                time.sleep(random.uniform(3.5, 4.5))

                if action in actions:
                    time.sleep(random.uniform(2, 3.5))
                    try:
                        # Locate the primary button based on the action
                        button = self.browser.find_element(By.XPATH, f"//header//*[@type='button']//*[contains(text(), '{actions[action]}')]")
                        if button.text == actions[action]:
                            button.click()
                            skip = False
                    except NoSuchElementException:
                        pass

                # action in popup window
                if action in ["unFollow", "removeRequest"]:
                    time.sleep(random.uniform(3.5, 4.5))
                    try:
                        path = action == "removeRequest" and "//*/button[contains(text(), 'Unfollow')]" or "//*/div[@role='button']//*[contains(text(), 'Unfollow')]"
                        popup_unfollow_button = self.browser.find_element(By.XPATH, path)
                        if popup_unfollow_button.text == "Unfollow":
                            popup_unfollow_button.click()
                            skip = False
                    except NoSuchElementException:
                        pass

                if action == "removeRequest":
                    self.re_write_pending_requests(user)
            except Exception as e:
                print(f"%s>>> Something went wrong on {action} action. Skipping...%s" % (fg(1), attr(0)))
                print(e)

            # Check action block
            try:
                time.sleep(random.uniform(5, 6.5))
                self.browser.find_element(By.TAG_NAME, "h3")
                print(f"%s\n>>> Instagram blocked {action} actions. Try again later. %s" % (fg(1), attr(0)))
                break
            except NoSuchElementException:
                pass

            # Check action block without popup
            try:
                time.sleep(random.uniform(3.5, 6.5))
                action_button = self.browser.find_element(By.XPATH, f"//header//*[@type='button']//*[contains(text(), '{actions[action]}')]")
                if action_button.text == actions[action]:
                    print(f"%s\n>>> Instagram blocked {action} actions. Try again later. %s" % (fg(1), attr(0)))
                    break
            except NoSuchElementException:
                pass

            # Check popup block
            if self.check_popup_block(action):
                return False

            count += 1
            self.mimic_mouse()

            # Wait for 25 seconds to avoid Instagram blocking actions, you can increase the time if you get blocked so often.
            # Please note that the more you increase the time, the more time it will take to finish the process.
            if skip:
                print(f"%s\n>>> Skipping {action} action cause it's already done. %s" % (fg(1), attr(0)))
                time.sleep(random.uniform(2.5, 3.5))
            else:
                sleepTime = math.floor(random.uniform(14, 32))
                for wait in range(sleepTime):
                    print(
                        f"%s>>> {
                     sleepTime-wait} seconds left to {action.lower()} next user... %s"
                        % (fg(2), attr(0)),
                        end="\r",
                    )
                    time.sleep(1)

    def collect_users(self, total, type):
        time.sleep(5)

        canCollectfollowers = True

        def scroll():
            if canCollectfollowers is False:
                self.browser.execute_script(_scripts.blockedFollowersScrollScript)
            else:
                self.browser.execute_script(_scripts.scrollScript)
                time.sleep(2)
                self.browser.execute_script(_scripts.scrollScript)
            time.sleep(2)

        # Check is followers available to collect
        try:
            self.browser.find_element(By.XPATH, "//*[@aria-label='Search input']")
        except NoSuchElementException:
            print(self.messages()["followersNotAvailable"])
            canCollectfollowers = False
            time.sleep(2)

        # If followers not available, collect only shown ones.
        if canCollectfollowers is False:
            scroll()
            total = self.browser.execute_script(_scripts.getChildElementCount)

        prev_count = 0

        # Start collecting
        while True:
            scroll()
            time.sleep(2)
            os.system("cls")

            new_count = len(self.browser.find_elements(By.XPATH, "//*[@class='x1rg5ohu']"))

            if prev_count == new_count:
                break

            prev_count = new_count

            print(f"%s>>> Collected {new_count} out of {total} {type} %s" % (fg(10), attr(0)))

            if new_count <= 1:
                break

            if new_count <= total:
                time.sleep(0.5)
            else:
                break

        followers = self.browser.find_elements(By.XPATH, "//*[@class='x1rg5ohu']")
        self.user_list = []

        i = 0
        for user in followers:
            link = user.find_element(By.TAG_NAME, "a").get_attribute("href")
            self.user_list.append(link)
            i += 1
            if i >= total:
                break

    def collect_followers(
        self,
    ):
        os.system("cls")
        self.browser.get(f"https://www.instagram.com/{self.username}/followers")
        time.sleep(3)

        self.messages()["countFollowers"]

        followers_count = len(self.browser.find_elements(By.XPATH, "//*[@class='x1rg5ohu']"))
        print(f">>> Started to Counting Followers: {followers_count}")

        while True:
            self.browser.execute_script(_scripts.scrollScript)
            time.sleep(2)
            self.browser.execute_script(_scripts.scrollScript)

            new_count = len(self.browser.find_elements(By.XPATH, "//*[@class='x1rg5ohu']"))
            self.clearc()

            if followers_count is not new_count:
                followers_count = new_count
                os.system("cls")
                print(
                    f"%s>>> Collected Followers: {
                 new_count}%s"
                    % (fg(10), attr(0))
                )
            else:
                break

        self.messages()["savingFollowers"]

        try:
            total_followers = self.browser.find_elements(By.XPATH, "//*[@class='x1rg5ohu']")

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
                if data["relationships_follow_requests_sent"][i]["string_list_data"][0]["href"] == user["string_list_data"][0]["href"]:
                    del data["relationships_follow_requests_sent"][i]
                    break

        # re-writing 'pending_follow_requests.json' file
        newFile = {"relationships_follow_requests_sent": data["relationships_follow_requests_sent"]}
        with open(self.requestedAccountsFilePath, "w", encoding="utf-8") as file:
            json.dump(newFile, file, indent=3)

    def get_username_password(self):
        if self.username and self.password:
            return

        print("%s\n>>> Please enter your Instagram credentials. %s" % (fg(171), attr(0)))
        self.username = _loginInfo.username if _loginInfo.username is not None else input("%susername: %s" % (fg(207), attr(0)))
        self.password = _loginInfo.password if _loginInfo.password is not None else input("%spassword: %s" % (fg(207), attr(0)))


try:
    igTool = InstagramTool()

    if __name__ == "__main__":
        try:
            while True:
                print("%s\n\n∴∵∴∵∴∵ INSTAGRAM TOOL ∴∵∴∵∴∵∴\n%s" % (fg(171), attr(0)))
                opt = input(
                    "%s"
                    "[1] - Download Profile Picture\n"
                    "[2] - Download Post (Picture)\n"
                    "[3] - Get Your Follower List\n"
                    "[4] - Follower Farm\n"
                    "[5] - Mass Unfollow \n"
                    "[6] - Remove Follow Requests\n"
                    "[7] - Show Pictures\n"
                    "[8] - Delete Pictures\n"
                    "[9] - Exit \n\n"
                    ">>> ENTER NUMBER: %s"
                    "" % (fg(171), attr(0))
                )

                if opt == "1":
                    # DOWNLOAD PROFILE PICTURE #
                    username = input("%susername: %s" % (fg(207), attr(0)))

                    igTool.download_pp(username)
                    igTool.reset_bot()
                elif opt == "2":
                    # DOWNLOAD POST #
                    link = input("%sPost Link: %s" % (fg(207), attr(0)))

                    igTool.downloadPost(link)
                    igTool.reset_bot()
                elif opt == "3":
                    # GET FOLLOWERS LIST #
                    igTool.get_username_password()

                    LOGGED = igTool.login()

                    if LOGGED:
                        igTool.collect_followers()
                        igTool.reset_bot()
                    else:
                        igTool.reset_bot()
                elif opt == "4":
                    # FOLLOW FARM #
                    igTool.get_username_password()

                    target = input("%sTarget account name: %s" % (fg(207), attr(0)))
                    total = int(input("%sTotal Follow: %s" % (fg(10), attr(0))))

                    LOGGED = igTool.login()
                    USER_EXIST = igTool.navigate_to(target, "followers")

                    if LOGGED & USER_EXIST:
                        igTool.collect_users(total, "Followers")
                        igTool.userAction("Follow")
                        print(igTool.messages()["done"])
                        igTool.reset_bot()
                    else:
                        igTool.reset_bot()
                elif opt == "5":
                    # MASS UNFOLLOW #
                    igTool.get_username_password()

                    total = int(input("%sTotal unFollow: %s" % (fg(10), attr(0))))

                    LOGGED = igTool.login()
                    USER_EXIST = igTool.navigate_to(igTool.username, "following")

                    if LOGGED & USER_EXIST:
                        igTool.collect_users(total, "Following")
                        igTool.userAction("unFollow")
                        print(igTool.messages()["done"])
                        igTool.reset_bot()
                    else:
                        igTool.reset_bot()
                elif opt == "6":
                    # REMOVE REQUESTS #
                    igTool.get_username_password()

                    LOGGED = igTool.login()

                    if LOGGED:
                        igTool.removeRequests()
                        print(igTool.messages()["done"])
                        igTool.reset_bot()
                    else:
                        igTool.reset_bot()
                elif opt == "7":
                    # OPEN SELECTED PICTURE #
                    igTool.show_img()
                elif opt == "8":
                    # DELETE SELECTED PICTURE #
                    igTool.delete_img()
                elif opt == "9":
                    igTool.close_bot()
                    exit()
        except KeyboardInterrupt:
            print("%s>>> Shutting down... %s" % (fg(10), attr(0)))
        except Exception as e:
            print("Caught an unexpected error: %s" % e)
            print("%s>>> Shutting down... %s" % (fg(10), attr(0)))
        finally:
            igTool.close_bot()
            exit()
except Exception as e:
    print(f"%s {e.msg} %s" % (fg(1), attr(0)))
