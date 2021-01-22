from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

username = "INSTAGRAM USERNAME HERE"
password = "INSTAGRAM PASSWORD HERE"

browserProfile = webdriver.ChromeOptions()
browserProfile.add_experimental_option('excludeSwitches',['enable-logging'])
browserProfile.add_experimental_option('prefs',{"intl.accept_languages":"en,en_US"})
browserProfile.add_argument("--headless")
browserProfile.add_argument("--disable-gpu")

def getFollowers(username,password):
    browser = webdriver.Chrome("driver/chromedriver.exe", chrome_options=browserProfile)
    browser.get("http://instagram.com/accounts/login")
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(username)
    browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(password)
    browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
    time.sleep(3)
    browser.get(f"https://www.instagram.com/{username}")
    time.sleep(2)

    browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
    time.sleep(2)

    actionBox = browser.find_element_by_css_selector("div[role=dialog] ul")
    CurrentFollowers = len(browser.find_elements_by_css_selector('li'))
    print(f"First Time Counting Followers: {CurrentFollowers}")

    action = webdriver.ActionChains(browser)

    while True:
        actionBox.click()
        action.key_down(Keys.PAGE_DOWN).key_down(Keys.PAGE_DOWN).key_down(Keys.PAGE_DOWN).perform()
        time.sleep(0.5)

        newCount = len(browser.find_elements_by_css_selector('li'))

        if CurrentFollowers != newCount:
            CurrentFollowers = newCount
            print(f"Counting Followers: {newCount}")
            time.sleep(0.5)
        else:
            break

    totalFollowers = actionBox.find_elements_by_css_selector('li')

    Flist = []
    i = 0
    for users in totalFollowers:
        i += 1
        if i == CurrentFollowers:
            break

        link = users.find_element_by_css_selector("a").get_attribute("href")
        Flist.append(link)


    with open("followers.txt","w",encoding="utf-8") as file:
        for item in Flist:
            file.write(item+ "\n")

    browser.close()
        


getFollowers(username,password)

