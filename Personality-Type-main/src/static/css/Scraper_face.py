from .Model import Model
from .Predict import Predictor
from selenium.webdriver import (Chrome, Firefox, ChromeOptions, FirefoxProfile)
#import pymongo
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

        #Initialize MongoDB
        #self.mongoClient = pymongo.MongoClient()
        #self.db = self.mongoClient['my-facebook-webscrape']
        #self.fb_statuses = self.db['fb-statuses']

        #dictyonari of statues
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

#--------------Terminar esto -----------------------
    def searched_statuses(self):
        #self.browser.find_element_by_css_selector(f'a[href="{self.first_profile_url}"]').click()
        #time.sleep(self.scroll_time)

        # Data structure of entry:
        #   {'name': STRING = name,
        #   'url': STRING = profile url,
        #   'datetime': DATETIME = current time,
        #   'statuses': DICT = {key=time of status post, value=status},
        #   'html': STRING = html of page,}
        #print("Url Anterior: " + str(self.browser.current_url))
        
        self.browser.get(self.first_profile_url)
        #print("Url Actual: " + str(self.browser.current_url))
        #input("Para")
        time.sleep(self.scroll_time)

        #Get scroll heigth
        #last_heigth = self.browser.execute_script("return document.body.scrollHeight")

        #Scroll through timeline and add statuses to dictionary
        #while len(self.dic_status.keys()) < self.number_status:

        Scroll_Pause_Time = self.scroll_time * (1 + random.random())

        #Scroll down to bottom
        # self.browser.execute_script("Window.scrollTo(0, document.body.scrollHeight);")

        #Weait to load page
        #time.sleep(Scroll_Pause_Time)

        print("--------Searching Post--------")
        #All_Post = self.browser.find_elements_by_tag_name('a')
        All_Post = self.browser.find_element_by_css_selector("div[id^='tl_unit_']")
                    
        #input("All_Post: " + str(All_Post))

        #for post in All_Post:
        try:       
            post_time_element = All_Post.find_element_by_css_selector('abbr')
            post_time = post_time_element.get_attribute('title')
            user_content_element = All_Post.find_element_by_css_selector("div.userContent")         
            para_elements = user_content_element.find_element_by_css_selector('p')
            #Status sometimes split in two p elements. Merge two paragraphs
            if para_elements is not None:
                text = ''            
                text += para_elements.text + ' '
            print('Date: ' + post_time + '\n' + 'Status: ' + text + '\n')
        
                #Add status to dictionary
            self.dic_status[post_time] = text
        except:
            print("Elements Not Found")

        print("Finished creating Statuses for: " + str(self.name))

        print("Final Dic: " + str(self.dic_status))

        save = open ('data/post.txt', 'w')
        save.write(text)
        save.close()   

        

    def predict_Face(self):
        p = Predictor()

        f = open ('data/post.txt','r')
        mensaje = f.read()
        print(mensaje)
        f.close()

        r = p.predict([mensaje])
        return r


def ExecFace():
    with open('Fb_login_creds.yaml', 'r') as credlog:
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
    return p
    #print("Prediccion: " + str(p))




if __name__ == '__main__':
    ExecFace()
    

