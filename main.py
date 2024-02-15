import os
import pygame
import speech_recognition as sr
from botScrapper import *
import pyautogui
import pywhatkit
import psutil
import win32gui
import win32con
from fuzzywuzzy import fuzz
from datetime import datetime

def speak(data):
    voice = 'en-US-GuyNeural' #en-US-GuyNeural #en-US-ChristopherNeural
    command = f'edge-tts --voice "{voice}" --text "{data}" --write-media "audio/data.mp3"'
    
    os.system(command)
    pygame.init()
    pygame.mixer.init()
    
    pygame.mixer.music.load("audio/data.mp3")
    
    try:
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(e)
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()

def takeCommand():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        speak('I am listening sir')
        print('Listening...')
        listener.pause_threshold = 1
        audioData = listener.listen(source)

        try:
            print('Recognizing...')
            query = listener.recognize_google(audioData, language='en-US')
        except Exception as e:
            print(e)
            return ""
        return query

def shutDown():
    speak('Very well sir i am shutting systems down')
    exit()

def aiResponse(query):
        sendQuery(query)
        isBubbleLoaderVisible()
        response = retrieveData()
        speak(response)

def isProcessRunning(processName):
    for process in psutil.process_iter(['name']):
        if process.info['name'].lower() == processName.lower():
            return True
    return False

def focusApp(appName):
    def callback(handleWindow, extraData):
        windowTitle = win32gui.GetWindowText(handleWindow).lower()
        ratio = fuzz.partial_ratio(appName.lower(), windowTitle)
        if ratio > 80:
            if win32gui.IsIconic(handleWindow):
                win32gui.ShowWindow(handleWindow, win32con.SW_RESTORE)
            win32gui.ShowWindow(handleWindow, win32con.SW_SHOW)
            # win32gui.BringWindowToTop(handleWindow)
            win32gui.SetForegroundWindow(handleWindow)
            print(f'I found the {appName}. It should be on your screen.')
            return True
    result = win32gui.EnumWindows(callback, None)
    if not result:
        print("No suitable matches found for", appName)

def openApp(query):
    appName = query.replace('open ', '')
    processName = appName + '.exe'
    if isProcessRunning(processName):
        speak(f' {appName} is already open. Let me find the app')
        focusApp(appName)
    else:
        try:
            speak('Opening ' + appName)
            pyautogui.press('super')
            pyautogui.sleep(0.5)
            pyautogui.typewrite(appName)
            pyautogui.sleep(0.7)
            pyautogui.press('enter')
        except Exception as e:
            speak(f"Sorry sir, I couldn't open {appName}. {str(e)}")
        
def gotoWebsite(query):
    openApp('open brave')
    siteName = query.replace('go to ', '')
    pyautogui.typewrite( 'https://' + siteName)
    pyautogui.press('enter')

def playOnYt(query):
    videoName = query.replace('play ', '')
    speak('Sure sir. Playing ' + videoName + ' on Youtube')
    pywhatkit.playonyt(videoName)

def getTime():
    currentTime = datetime.now().strftime('%H:%M')
    speak(f'Current Time is {currentTime}')
    
def closeApp():
        speak('Right away sir')
        pyautogui.hotkey('alt', 'f4')
        # pyautogui.moveTo(1895, 10)
        # pyautogui.click()

sleepMode = False

speak('Allow me to introduce myself, i am Jarvis, a Virtual Artificial intelligence and i am here to assist you with a variety of tasks as best i can.')

clickChatButton()
while True:
    query = input('You: ') # takeCommand().lower()
    print('\nYou: ' + query)
    
    if 'exit' in query:
        shutDown()
    elif 'open' in query:
        openApp(query)
    elif 'change tab'  in query:
        pyautogui.hotkey('alt', 'tab')
    elif 'switch tab' in query:
        pyautogui.hotkey('ctrl', 'tab')
    elif 'close tab' in query:
        pyautogui.hotkey('ctrl', 'w')
    elif 'go to' in query:
        gotoWebsite(query)
    elif 'play' in query:
        playOnYt(query)
    elif 'time' in query:
        getTime()   
    elif 'close' in query:
        closeApp()
    elif 'sleep' in query:
        speak('Ok sir. I will sleep but you can call me any time just say a word.')
        sleepMode = True
    else:
        aiResponse(query)
    while sleepMode:
        query = input('You: ') # takeCommand().lower()
        if 'wake up' in query:
            speak('How can i help you sir.')
            sleepMode = False