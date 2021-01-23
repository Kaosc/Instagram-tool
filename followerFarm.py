from .info import username, password, target, unfTarget
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import warnings
from colored import fg, attr
import os

warnings.filterwarnings("ignore", category=DeprecationWarning)

class FollowBot:

    def __init__(self):
        self.mainList = []
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_argument("--disable-gpu")
        self.browserProfile.add_argument("--headless")
        self.browserProfile.add_argument("--lang=en")
        self.browserProfile.add_experimental_option('excludeSwitches',['enable-logging'])
        self.browserProfile.add_experimental_option('prefs',{"intl.accept_languages":"en,en_US"})

    def login(self,username,password):
        os.system('cls')
        self.browser = webdriver.Chrome("chromedriver.exe", chrome_options=self.browserProfile)
        print("%s--> Login in\n%s" % (fg(61), attr(0)))
        self.username = username
        self.password = password
        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(self.username)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(self.password)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
        time.sleep(3)

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

bot = FollowBot()

while True:
    print("\n%s - - IG BOT - -  %s\n" % (fg(119), attr(0)))
    sc = input("%s[1] - Follow\n[2] - Unfollow\n[3] - Exit\n%s\nEnter Number: " % (fg(119), attr(0)))
    if sc == "3":
        exit()
    else:
        if sc == "1":
            total = int(input("%sTotal Follow: %s" % (fg(10), attr(0))))
            bot.login(username,password)
            bot.navigateFollowers(target)
            bot.getUserList(total)
            bot.follow()
            bot.message()
            bot.closeBot()
        elif sc == "2":
            total = int(input("%sTotal unFollow: %s" % (fg(10), attr(0))))
            bot.login(username,password)
            bot.navigateFollowings(unfTarget)
            bot.getUserList(total)
            bot.unFollow()
            bot.message()
            bot.closeBot()

