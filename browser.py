from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import os

link: str = 'https://www.twitch.tv/warframe'
duration: int = 15
# As chrome refuses to open another window with the same profile if a chrome window is already open,
# User Data folder was duplicated to generate a separate profile for automation purpose
# TODO:
# 1. Need to create checks for existing chrome windows and handle this better
# 2. Make a browser class so that its easier to switch browser

profile_path = os.environ.get('LOCALAPPDATA') + r'\Google\Chrome\AutomationGV'
profile_name = 'Default' #not implemented
app = 'Chrome'

# print("Variables defined")

def init_browser(browser: str, path: str, profile: str ='Default'):
    '''
    Starts a webdriver instance for specified browser name

    NOTE : call just before starting the stream to reduce resource usage and prevent duplicate
    windows of the same app. Causes issues with Selenium.
    '''
    browser = browser.lower()
    match browser:
        case 'chrome':
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            options.add_argument(r"--user-data-dir=" + path)
            options.add_argument(r"--profile-directory=" + profile)
            options.add_experimental_option("detach",True)
            # options.add_argument("--no-sandbox")
            # options.add_argument("--disable-dev-shm-usage")  #TODO: Uncomment for linux
            print(f'Using profile at {path}')
            driver = webdriver.Chrome(service= service, options= options)
            return driver
        case 'firefox':
            # TODO: add firefox support
            raise NotImplementedError('Firefox support needs to be implemented')
        case _:
            # raise Exception("Undefined browser type. Only Chrome is supported currently")
            return browser

# TODO: Update play_stream and include it as part of Stream class method so that it uses Stream attributes
# @deprecated
def play_stream(link: str, duration: int, browser: webdriver) -> None:
    print('defined play_stream')
    driver = browser
    driver.get(url = link)
    print(duration)
    # sleep(duration)
    # driver.close()

# def main() -> None:
#     print('Running main')
#     try:
#         browser = init_browser(browser= app, path= profile_path, profile= profile_name)
#         play_stream(link, duration, browser)
#     except Exception as e:
#         print(e)

# if __name__ == '__main__':
#     main()
