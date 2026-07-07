import pyttsx3
import random
import re
import smtplib
import winsound
import wikipedia
import sys
import os
import webbrowser
import datetime
import speech_recognition as sr
from urllib.request import urlopen
from PyQt5 import QtWidgets, QtGui,QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from geopy import Nominatim
from pip._vendor import requests
from bs4 import BeautifulSoup as soup
from yahoo_fin import stock_info


flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
engine.setProperty('rate',180)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour <12:
        speak("hello sir Good morning i am jarvis")
    elif hour>=12 and hour<18:
        speak("hello sir Good Afternoon i am jarvis")
    else:
        speak("hello sir Good evening i am jarvis")

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('naugraiyasuryansh@gmail.com', '6394682401')
    server.sendmail('naugraiyasuryansh@gmail.com', to, content)
    server.close()

class mainT(QThread):
    def __init__(self):
        super(mainT,self).__init__()
    
    def run(self):
        self.JARVIS()
    
    def STT(self):
        R = sr.Recognizer()
        with sr.Microphone() as source:
            speak("please tell me what to do")
            audio = R.listen(source)
        try:
            speak("wait Recognizing")
            text = R.recognize_google(audio,language='en-in')
        except Exception:
            return "none"
        text = text.lower()
        return text

    def JTT(self):
        R = sr.Recognizer()
        with sr.Microphone() as source:
            speak("listening")
            audio = R.listen(source)
        try:
            speak("wait Recognizing")
            text1 = R.recognize_google(audio,language='en-in')
        except Exception:
            speak("not able to recognize")
            return ""
        text1 = text1.lower()
        return text1

    def JARVIS(self):
        speak("starting")
        speak("initiating the system")
        speak("loading")
        wish()
        while True:

            self.query = self.STT()

            if ('bye' in self.query or 'quit' in self.query or 'bye bye'in self.query or 'leave' in self.query or "nothing" in self.query or "shutdown" in self.query):
                speak('Bye Sir. Have a nice day')
                winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                sys.exit()

            elif ("hello" in self.query):
                hour = int(datetime.datetime.now().hour)
                if hour >= 0 and hour < 12:
                    speak("hello sir Good morning")
                elif hour >= 12 and hour < 18:
                    speak("hello sir Good Afternoon")
                else:
                    speak("hello sir Good evening")

            elif ('music' in self.query or 'refresh' in self.query or 'anything' in self.query or 'song' in self.query):
                if('music' in self.query or 'song' in self.query):
                    speak("wait i am playing music")
                else:
                    speak("ok then i am playing music to refresh ur mind")
                self.music_dir ="D:\\SONGS\\English Songs"
                self.musics = os.listdir(self.music_dir)
                num = random.randint(0, 11)
                os.startfile(os.path.join(self.music_dir,self.musics[num]))

            elif 'wikipedia' in self.query:
                self.query = self.query.replace("wikipedia", "")
                if self.query:
                    speak("Searching Wikipedia...")
                    self.results = wikipedia.summary(self.query, sentences=2)
                    speak("According to Wikipedia")
                    speak(self.results)
                else:
                    speak("sorry sir not recognizing")
                    pass

            elif 'time' in self.query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak("The time is: ")
                speak(strTime)

            elif 'launch vs code' in self.query:
                speak("please wait i am launching v s code")
                self.codepath = "C:\\Users\\snaug\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code"
                os.startfile(self.codepath)

            elif ('launch java') in self.query:
                speak("please wait i am launching intelli j")
                self.codepath = "C:\\Program Files\\JetBrains\\IntelliJ IDEA 2020.1.1\\bin\\idea64.exe"
                os.startfile(self.codepath)

            elif ('launch notepad') in self.query:
                speak("please wait i am launching notepad")
                self.codepath = "C:\\Users\\snaug\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Accessories\\notepad"
                os.startfile(self.codepath)

            elif 'email' in self.query:
                try:
                    speak("What should i say?")
                    self.content = self.STT()
                    to = "snaugraiya10@gmail.com"
                    sendEmail(to, self.content)
                    speak("Email has been sent!")
                except Exception as e:
                    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                    speak("Sorry! i m not able to send this email")
                    pass

            elif 'open' in self.query:
                speak("please wait")
                self.reg_ex = re.search('open (.+)', self.query)
                if self.reg_ex:
                    self.domain = self.reg_ex.group(1)
                    if (self.domain == "youtube"):
                        speak("what to search")
                        self.line = self.JTT()
                        if self.line:
                            speak("Hold on, searching " + self.line)
                            self.url = "https://www.youtube.com/results?search_query=" + self.line
                            webbrowser.open(self.url)
                        else:
                            speak("so opening youtube")
                            self.url = "https://www.youtube.com"
                            webbrowser.open(self.url)
                    elif (self.domain == "google"):
                        speak("what to search")
                        self.line = self.JTT()
                        if self.line:
                            speak("Hold on, searching " + self.line)
                            self.url = 'https://www.google.com/search?q=' + self.line
                            webbrowser.open(self.url)
                        else:
                            speak("so opening google")
                            self.url = "https://www.google.com"
                            webbrowser.open(self.url)
                    else:
                        self.url = "https://www." + self.domain + ".com"
                        webbrowser.open(self.url)
                        speak('The website you have requested has been opened for you Sir.')
                else:
                    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                    speak("sorry sir not able to recognize")
                    pass

            elif 'joke' in self.query:
                speak("please wait searching for joke")
                res = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "application/json"})
                if res.status_code == requests.codes.ok:
                    speak(str(res.json()['joke']))
                    winsound.PlaySound('hahaha.wav', winsound.SND_FILENAME|winsound.SND_NOWAIT)

                else:
                    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                    speak('oops!I ran out of jokes')
                    pass

            elif 'news' in self.query:
                speak("please wait sir searching for latest news")
                try:
                    news_url = "https://news.google.com/news/rss"
                    Client = urlopen(news_url)
                    xml_page = Client.read()
                    Client.close()
                    soup_page = soup(xml_page, "xml")
                    news_list = soup_page.findAll("item")
                    speak("latest news is")
                    for news in news_list[:2]:
                        print(news.title.text)
                        print("-" * 60)
                        speak(news.title.text.encode('utf-8'))
                except Exception as e:
                    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                    speak("sorry sir not able to get the news")
                    pass

            elif ('weather' in self.query or 'temperature' in self.query):
                api_key = "54b1b9aeefe8b01a10b622d47828ef3d"
                base_url = "http://api.openweathermap.org/data/2.5/weather?"
                speak("which city sir")
                city_name = self.JTT()
                if city_name:
                    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
                    response = requests.get(complete_url)
                    x = response.json()
                    if x["cod"] != "404":
                        y = x["main"]
                        c_temperature = y["temp"] - 272.15
                        current_temperature = "{:.2f}".format(c_temperature)
                        z = x["weather"]
                        weather_description = z[0]["description"]
                        speak(" Temperature (in celcius unit) = " +
                              str(current_temperature) +
                              "\n description = " +
                              str(weather_description))
                    else:
                        winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                        speak(" City Not Found Sir ")
                        pass
                else:
                    pass

            elif 'help me' in self.query:
                speak("""
                        You can use these commands and I'll help you out:
                        1. bye/ bye bye/ leave/ quit/ shutdown/ nothing : to stop the program
                        2. Open xyz : replace xyz with any website name
                        3. email : Follow up questions such as recipient name, content will be asked in order.
                        4. weather/temperature : Tells you the current condition and temperture
                        5. music/ song/ anything/ refresh/ song : to randomly play a song
                        6. wikipedia xyz : to search xyz on wikipedia
                        7. google xyz : search xyz on google
                        8. news : top news of today
                        9. time : Current system time
                        10. city/ state/ location : to find the location of that city/ state
                        11. joke : to tell joke
                        12. stock : to know the current stock price of amazon
                        13. hello : i will greet you
                        14. launch xyz : to open xyz app
                        15. who are you/ about youself : to know about me
                        16. your age/ old : to know my age
                        17. good/ keep it up/ well done : to praise me
                        """)

            elif ('city' in self.query or 'state' in self.query or 'location' in self.query):
                geolocator = Nominatim(user_agent="geoapiExercises")
                speak("PLease tell city or state name")
                self.line = self.JTT()
                if self.line:
                    location = geolocator.geocode(self.JTT())
                    speak("Country location is:" + str(location))
                else:
                    pass

            elif "google" in self.query:
                reg_ex = re.search("google (.+)", self.query)
                if reg_ex:
                    search = reg_ex.group(1)
                    speak("Hold on, I will search " + search)
                    url = 'https://www.google.com/search?q=' + search
                    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
                    webbrowser.get('chrome').open_new_tab(url)
                else:
                    speak("sorry sir not able to recognize")
                    pass

            elif "stock" in self.query:
                stock_info.get_live_price("AMZN")
                speak("stock price of amazon is")
                speak(str(stock_info.get_live_price("AMZN")))

            elif ("about yourself" in self.query or "who are you" in self.query):
                speak("hi, i m jarvis. i m the personal assistant of suryansh sir. i m multitalented")

            elif ("your age" in self.query or "old" in self.query):
                speak("i am immortal sir")

            elif ('good' in self.query or 'keep it up' in self.query or 'well done' in self.query):
                speak("thank u sir")

            elif "none" in self.query:
                pass

            else:
                winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                speak("sorry sir not able to recognize")


FROM_MAIN,_ = loadUiType(os.path.join(os.path.dirname(__file__),"./scifi.ui"))

class Main(QMainWindow,FROM_MAIN):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(1920,1080)
        self.label_8 = QLabel
        self.exitB.setStyleSheet("background-image:url(./lib/exit.png);\n"
        "border:none;")
        self.exitB.clicked.connect(self.close)
        self.setWindowFlags(flags)
        Dspeak = mainT()
        self.label_8 = QMovie("./lib/initiating system.gif", QByteArray(), self)
        self.label_8.setCacheMode(QMovie.CacheAll)
        self.label_6.setMovie(self.label_8)
        self.label_8.start()
        self.label_9 = QMovie("./lib/loading.gif", QByteArray(), self)
        self.label_9.setCacheMode(QMovie.CacheAll)
        self.label_7.setMovie(self.label_9)
        self.label_9.start()
        Dspeak.start()
        self.label.setPixmap(QPixmap("./lib/tuse.png"))

app = QtWidgets.QApplication(sys.argv)
main = Main()
main.show()
exit(app.exec_())