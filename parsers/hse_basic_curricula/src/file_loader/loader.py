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
            _load_hse('https://asav.hse.ru/basicplans.html?faculty=&regdepartment=', 'showBasicFaculty', path, headless)
    
        case PlanType.HSE_PLAN:
            _load_hse('https://asav.hse.ru/plans.html?login=web&password=web', 'showWorkFaculty', path, headless)



# The only thing different between plans and basic plans is that hyperlinks call different js functions so :hyp_signature contains functions's name
def _load_hse(url, hyp_signature, path: str, headless: bool = False):
    browser = _setup_chrome_driver(path, headless)
    
    browser.get(url)
    
    print('Opened web page')

    try:
        print('Started loading hrefs to download pdfs')
        
        # When page is opened it loads data for some time so we have to wait until hyperlinks appear
        element = WebDriverWait(browser, 8).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '" + hyp_signature + "')]")))
        
        # execute_script is used instead of element.click() because element.click() for some reason can't track position of elements correctly
        for element in browser.find_elements(By.XPATH, "//a[contains(@href, '" + hyp_signature + "')]"):
            browser.execute_script("arguments[0].click();", element)
        
        # When hyperlink is clicked it loads table for some time so we wait until there is not a single element on page with id = "workTableLoading"
        WebDriverWait(browser, 20).until_not(EC.visibility_of_element_located((By.XPATH, '//tr[@id = "workTableLoading"]')))
        print('Finished loading hrefs to download pdfs')
        print("Started downloading pdfs")

        # Downloading all at once can make browser lag so pdfs are loaded one by one
        for element in browser.find_elements(By.XPATH, '//a[contains(@href, "executeUnitedPlan") and @milldata="DescriptionAsPDF"]'):
            start_time = time.time()
            
            # Clicking on download link opens a new tab, which will close when download is finished
            # So to check if download is finished, we can just check if number of tabs is equal to 1
            browser.execute_script("arguments[0].click();", element)
            WebDriverWait(browser, 60).until(lambda x: len(x.window_handles) <= 1) 
            
            print("--- %s seconds ---" % (time.time() - start_time))

        print("Download finished!")
    except TimeoutException:
        print("Loading took too much time!")



def _setup_chrome_driver(path: str, headless: bool = False) -> WebDriver:
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