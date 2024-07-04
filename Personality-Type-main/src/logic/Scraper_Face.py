from .Predict import Predictor
from selenium.webdriver import (Chrome, Firefox, ChromeOptions, FirefoxProfile)
import datetime
import yaml
import time
import random

class FBScraper():
    def __init__(self, email, password, profile, status = 4, scroll_time = 7, browser= 'Firefox'):
        self.first_email = email
        self.first_password = password
        self.first_profile_url = profile
        self.number_status = status
        self.scroll_time = scroll_time
        self.name = profile.split("/")[3]
 
        y = self.set_browser(browser)
        self.dic_status = {}

    def set_browser(self, browser):
        #Firefox
        if browser == 'Firefox':
            profile = FirefoxProfile()
            profile.set_preference("dom.webnotifications.enabled", False)
            self.browser = Firefox(firefox_profile=profile)
            
        #Chrome
        if browser == 'Chrome':
            options = ChromeOptions()
            options.add_argument("--disable-notifications")
            self.browser = Chrome(options=options)
    
    def open_fb(self):
        #Login to FB in Selenium Browser
        url = 'http://www.facebook.com/'
        self.browser.get(url)

        email =self.browser.find_element_by_id('email')
        password = self.browser.find_element_by_id('pass')

        email.send_keys(self.first_email)
        password.send_keys(self.first_password)

        self.browser.find_element_by_id("loginbutton").click()

def searched_statuses(self):
        self.browser.get(self.first_profile_url)
        time.sleep(self.scroll_time)

        Scroll_Pause_Time = self.scroll_time * (1 + random.random())

        print("--------Searching Post--------")
        All_Post = self.browser.find_element_by_css_selector("div[id^='tl_unit_']")

        try:       
            post_time_element = All_Post.find_element_by_css_selector('abbr')
            post_time = post_time_element.get_attribute('title')
            user_content_element = All_Post.find_element_by_css_selector("div.userContent")         
            para_elements = user_content_element.find_element_by_css_selector('p')

            if para_elements is not None:
                text = ''            
                text += para_elements.text + ' '
            print('Date: ' + post_time + '\n' + 'Status: ' + text + '\n')

            self.dic_status[post_time] = text
        except:
            print("Elements Not Found")

        print("Finished creating Statuses for: " + str(self.name))

        print("Final Dic: " + str(self.dic_status))

        save = open ('logic/data/post.txt', 'w')
        save.write(text)
        save.close()   

def predict_Face(self):
        p = Predictor()
        f = open ('logic/data/post.txt','r')
        mensaje = f.read()
        print(mensaje)
        f.close()

        r = p.predict([mensaje])
        return r

def ExecFace():
    with open('logic/fb_login_creds.yaml', 'r') as credlog:
        try:
            yread = yaml.load(credlog, Loader=yaml.FullLoader)
            password = yread['password']
            email = yread['email']
            profile = yread['profile_url']
        except yaml.YAMLError as exc:
            print(exc)

    FBS = FBScraper(email = email, password = password, profile = profile, browser = 'Firefox')
    FBS.open_fb()
    FBS.searched_statuses()
    p = FBS.predict_Face()
    print("Prediccion: " + str(p))

if __name__ == '__main__':
    ExecFace()