from selenium import webdriver #selenium 4.13.0
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from plan_types import PlanType


def load(plan_type: PlanType, path: str, headless: bool):
    match plan_type:
        case PlanType.HSE_BASIC_PLAN:
            __load_hse('https://asav.hse.ru/basicplans.html?faculty=&regdepartment=', 'showBasicFaculty', path, headless)
    
        case PlanType.HSE_PLAN:
            __load_hse('https://asav.hse.ru/plans.html?login=web&password=web', 'showWorkFaculty', path, headless)


def __load_hse(url, hyp_signature, path: str, headless: bool = False):
    browser = __setup_chrome_driver(path, headless)
    browser.get(url)

    try:
        # Wait for page to load and hyperlinks to appear
        element = WebDriverWait(browser, 8).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '" + hyp_signature + "')]")))
        
        for element in browser.find_elements(By.XPATH, "//a[contains(@href, '" + hyp_signature + "')]"):
            browser.execute_script("arguments[0].click();", element)
        
        # Wait for all tables to load
        WebDriverWait(browser, 20).until_not(
            EC.visibility_of_element_located((By.XPATH, '//tr[@id = "workTableLoading"]')))
        print("Started downloading pdfs")

        # Downloading all at once can make browser lag so pdfs are loaded one by one
        href_xpath = '//a[contains(@href, "executeUnitedPlan") and @milldata="DescriptionAsPDF"]'
        for element in browser.find_elements(By.XPATH, href_xpath):
            start_time = time.time()
            
            # Download is finished when tab count is equal to 1
            browser.execute_script("arguments[0].click();", element)
            WebDriverWait(browser, 60).until(lambda x: len(x.window_handles) <= 1) 
            
            print("--- %s seconds ---" % (time.time() - start_time))

        print("Download finished")
    except TimeoutException:
        print("Loading took too much time")


def __setup_chrome_driver(path: str, headless: bool = False) -> WebDriver:
    print('Started setting up chrome driver')
    chrome_options = Options()
    
    # Options to run webdriver without browser window opening
    if headless:
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--disable-gpu')
        
    # Options that disable download popups and set download directory to :path
    prefs = {
        "profile.default_content_settings.popups":0,
        "download.prompt_for_download": "false",
        "download.default_directory" : path
        }
    chrome_options.add_experimental_option("prefs",prefs)
    
    # Install chrome driver and get webdriver instance from it
    chrome_service = ChromeService(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    
    # Required to download files in headless mode
    if headless:
        browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': path}}
        browser.execute("send_command", params)
    
    print('Finished setting up chrome driver')
    return browser