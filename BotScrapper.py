from time import sleep
import warnings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

warnings.simplefilter("ignore")
url = f'https://cdn.botpress.cloud/webchat/v1/index.html?options=%7B%22config%22%3A%7B%22composerPlaceholder%22%3A%22Talk%20to%20JARV%C4%B0S%22%2C%22botConversationDescription%22%3A%22Virtual%20Artificial%20Intelligence%22%2C%22botId%22%3A%224d846817-cd2d-4fae-a793-f59676b77c19%22%2C%22hostUrl%22%3A%22https%3A%2F%2Fcdn.botpress.cloud%2Fwebchat%2Fv1%22%2C%22messagingUrl%22%3A%22https%3A%2F%2Fmessaging.botpress.cloud%22%2C%22clientId%22%3A%224d846817-cd2d-4fae-a793-f59676b77c19%22%2C%22webhookId%22%3A%224531bafb-46e0-459c-9cc5-29f0c94ebfa9%22%2C%22lazySocket%22%3Atrue%2C%22themeName%22%3A%22prism%22%2C%22botName%22%3A%22Jarvis%22%2C%22stylesheet%22%3A%22https%3A%2F%2Fwebchat-styler-css.botpress.app%2Fprod%2Fcc4fc173-db4e-43ca-82cf-f837c9fdb767%2Fv51471%2Fstyle.css%22%2C%22frontendVersion%22%3A%22v1%22%2C%22theme%22%3A%22prism%22%2C%22themeColor%22%3A%22%232563eb%22%2C%22chatId%22%3A%22bp-web-widget%22%2C%22encryptionKey%22%3A%221tSzO6y2fX6nxALiQTQtQ4wMqtEPHnAe%22%7D%7D'
chromeDriverPath = 'chromedriver.exe'
chromeOptions = Options()
chromeOptions.add_argument("--headless=new")
chromeOptions.add_argument('--log-level=3')
service = Service(chromeDriverPath)
userAgent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
chromeOptions.add_argument(f'user-agent={userAgent}')
driver = webdriver.Chrome(service=service, options=chromeOptions)
driver.maximize_window()
driver.get(url)
sleep(3)

def clickChatButton():
    button = driver.find_element(By.XPATH, '/html/body/div/div/button').click()
    sleep(2)
    while True:
        try:
            loader = driver.find_element(By.CLASS_NAME, 'bpw-msg-list-loading')
            isVisible = loader.is_displayed
            print('Initializing Jarvis...')
            
            if not isVisible:
                break
            else:
                pass
        except NoSuchElementException:
            print('Jarvis is now fully operational')
            break
        sleep(1)
        
def sendQuery(text):
    textArea = driver.find_element(By.ID, 'input-message')
    textArea.send_keys(text)
    sleep(1)
    
    sendBtn = driver.find_element(By.ID, 'btn-send').click()
    sleep(1)
    
def isBubbleLoaderVisible():
    print('Jarvis is thinking...')
    while True:
        try:
            bubbleLoader = driver.find_element(By.CLASS_NAME, 'bpw-typing-group')
            isVisible = bubbleLoader.is_displayed
            
            if not isVisible:
                break
            else:
                pass
        except NoSuchElementException:
            print('Jarvis is answering')
            break
        sleep(1)
        
chatNumber = 2

def retrieveData():
    print('Retrieving Chat...')
    global chatNumber
    sleep(1)
    rData = driver.find_element(By.XPATH, f'/html/body/div/div/div/div[2]/div[1]/div/div/div[{chatNumber}]/div/div[2]/div/div/div/div/div/p')
    print('\nJarvis: ' + rData.text)
    chatNumber = chatNumber + 2
    return(rData.text)
