from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement
import time, sys, io
from plan_types import PlanType
from pathlib import Path
import re

def load(plan_type: PlanType, path: str, headless: bool):
    match plan_type:
        case PlanType.HSE_BASIC_PLAN:
            __load_hse('https://asav.hse.ru/basicplans.html?faculty=&regdepartment=', 'showBasicFaculty', path, headless)
    
        case PlanType.HSE_PLAN:
            __load_hse('https://asav.hse.ru/plans.html?login=web&password=web', 'showWorkFaculty', path, headless)


def __load_hse(url: str, hyp_signature: str, path: str, headless: bool = False):
    """_summary_

    Args:
        url (str): url to HSE plans
        hyp_signature (str): used to find links to expand tables
        path (str): download path
        headless (bool, optional): if true browser will run without displaying window
    """
    
    # Get existing files in the folder to skip them when downloading files
    existing_files = ''
    checked_files = ''
    
    if Path(path).exists():
        for item in Path(path).glob('*.pdf'):
            existing_files += item.name + '\n'

    browser = __setup_chrome_driver(path, headless)
    browser.get(url)
    
    try:
        # Wait for page to load and hyperlinks to appear
        element = WebDriverWait(browser, 8).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '" + hyp_signature + "')]")))
        
        # Click an all links that expand tables with pdfs
        for element in browser.find_elements(By.XPATH, "//a[contains(@href, '" + hyp_signature + "')]"):
            browser.execute_script("arguments[0].click();", element)
        
        # Wait for all tables to load
        WebDriverWait(browser, 20).until_not(
            EC.visibility_of_element_located((By.XPATH, '//tr[@id = "workTableLoading"]')))
        # Sleeep for 10 seconds because wainting with selenium is not enough
        time.sleep(10)
        print("Started downloading pdfs")
        
        # Iterate over all download links
        download_links = browser.find_elements(By.XPATH, '//a[contains(@href, "executeUnitedPlan") and @milldata="DescriptionAsPDF"]')
        
        total = len(download_links)
        current = 1
        new_count = 0
        
        for element in download_links:
            start_time = time.time()
            
            # Check if pdf is already downloaded and click if not
            #if not __check_if_downloaded(element, existing_files):
            
            re_groups = re.search(r"'.*?'", element.get_attribute('outerHTML'))
            if re_groups is not None:
                name = re_groups.group(0)[1:-1].replace(':', '').replace('&quot;', '').replace('/', ' ') + '.pdf'
                print(name)
                
                # Check if file is already downloaded
                # However sometimes files have similar names but different contents
                # So if we already checked the name, then it's probably a new file and we should download it
                if not name in existing_files or name in checked_files:
                    browser.execute_script("arguments[0].click();", element)
                    WebDriverWait(browser, 60).until(lambda x: len(x.window_handles) <= 1)
                    new_count += 1
                    print("New №" + str(new_count))
                    
                checked_files += name + '\n'
            
            print("--- %s seconds (%s/%s) ---" % (time.time() - start_time, current, total))
            current += 1

        print("Download finished")
        print("Downloaded: " + str(new_count))
    except TimeoutException:
        print("Loading took too much time")


def __check_if_downloaded(element: WebElement, existing_files: str) -> bool:
    """Check if element on click will download a file that already exists

    Args:
        element (WebElement): element that can be clicked to download a plan pdf
        existing_files (str): string with all the files that were downloaded before script started

    Returns:
        bool: true if click on element will download a file that already exists
    """
    
    re_groups = re.search(r"'.*?'", element.get_attribute('outerHTML'))
    if re_groups is not None:
        name = re_groups.group(0)[1:-1].replace(':', '').replace('&quot;', '').replace('/', ' ') + '.pdf'
        print(name)
        return name in existing_files
            
    return False


def __setup_chrome_driver(path: str, headless: bool = False) -> WebDriver:
    """Setup chrome driver for selenium

    Args:
        path (str): download folder path
        headless (bool, optional): if true browser will run without displaying window

    Returns:
        WebDriver: Chrome driver
    """
    
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