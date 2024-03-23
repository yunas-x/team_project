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
import time
from enums import PlanType
from pathlib import Path
import re
import logging
from config import HSE_ANNUAL_URL, HSE_BASIC_URL
from loaders.base import BaseLoader
from abc import ABC, abstractmethod


class HseBaseLoader(BaseLoader, ABC):
    """Base HSE loader"""
    
    def load(self, path: str) -> None:
        self.__load_hse(self._url, self._hyp_signature, path, True)
    
    
    @property
    @abstractmethod
    def _url(self) -> str:
        """Property for getting url"""
        
        
    @property
    @abstractmethod
    def _hyp_signature(self) -> str:
        """Property for getting hyperlink signature that is used to find download links"""
    
    
    def __load_hse(self, url: str, hyp_signature: str, path: str, headless: bool = False):
        """Method to download HSE annual/basic plans

        Args:
            url (str): url to HSE plans
            hyp_signature (str): used to find links to expand tables
            path (str): download path
            headless (bool, optional): if true browser will run without displaying window
        """
        
        # Get existing files in the folder to skip them when downloading files
        existing_files = self.__get_existing_files_string(path)
        checked_files = ''

        browser = self.__setup_chrome_driver(path, headless)
        browser.get(url)
        
        try:
            # Wait for page to load and hyperlinks to appear
            element = WebDriverWait(browser, 8).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '" + hyp_signature + "')]")))
            
            # Click all links to expand tables with pdfs
            for element in browser.find_elements(By.XPATH, "//a[contains(@href, '" + hyp_signature + "')]"):
                browser.execute_script("arguments[0].click();", element)
            
            # Wait for all tables to load
            WebDriverWait(browser, 20).until_not(
                EC.visibility_of_element_located((By.XPATH, '//tr[@id = "workTableLoading"]')))
            # Sleeep for 10 seconds because waiting with selenium is not enough
            time.sleep(10)
            logging.info("Started downloading pdfs")
            
            # Iterate over all download links
            download_links = browser.find_elements(By.XPATH, '//a[contains(@href, "executeUnitedPlan") and @milldata="DescriptionAsPDF"]')
            
            total = len(download_links)
            current = 1
            new_count = 0
            
            for element in download_links:
                start_time = time.perf_counter()
                
                # Getting the file name from outerHTML and not from href, because encoding breakes when using get_attribute on actual attributes
                re_groups = re.search(r"'.*?'", element.get_attribute('outerHTML'))
                if re_groups is not None:
                    name = re_groups.group(0)[1:-1].replace(':', '').replace('&quot;', '').replace('/', ' ') + '.pdf'
                    logging.info('')
                    logging.info('--- %s/%s ---' % (current, total))
                    logging.info(f"Checking {name}")
                    
                    # Check if file is already downloaded
                    # However sometimes files have similar names but different contents
                    # So if we already checked the name, then it's probably a new file and we should download it
                    if not name in existing_files or name in checked_files:
                        logging.info('NEW - Started downloading')
                        browser.execute_script("arguments[0].click();", element)
                        WebDriverWait(browser, 60).until(lambda x: len(x.window_handles) <= 1)
                        new_count += 1
                        logging.info('Finished')
                    else:
                        logging.info('EXISTS')
                        
                    checked_files += name + '\n'
                
                logging.info("--- %s seconds [New: %s] ---" % (time.perf_counter() - start_time, new_count))
                current += 1

            logging.info("Download finished")
            logging.info("Downloaded: " + str(new_count))
        except TimeoutException:
            logging.info("Loading took too much time")
        except:
            logging.exception("Exception has been encountered")


    def __get_existing_files_string(self, path: str) -> str:
        """Returns a string with names of all files in a folder, separated by '|'

        Args:
            path (str): path to a folder

        Returns:
            str: String with names of all files in a folder, separated by '|'
        """
        existing_files = ''
        if Path(path).exists():
            for item in Path(path).glob('*.pdf'):
                existing_files += item.name + '\n'
        return existing_files

    def __setup_chrome_driver(self, path: str, headless: bool = False) -> WebDriver:
        """Setup chrome driver for selenium

        Args:
            path (str): download folder path
            headless (bool, optional): if true browser will run without displaying window

        Returns:
            WebDriver: Chrome driver
        """
        
        logging.info('Started setting up chrome driver')
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
        
        logging.info('Finished setting up chrome driver')
        return browser
    
    
class HseAnnualLoader(HseBaseLoader):
    """Class for loading annual study plans for HSE"""
    
    @property
    def _url(self) -> str:
        return HSE_ANNUAL_URL
    
    @property
    def _hyp_signature(self) -> str:
        return 'showWorkFaculty'
    
    # def load(path: str) -> None:
    #     __load_hse(HSE_ANNUAL_URL, 'showWorkFaculty', path, True)


class HseBasicLoader(HseBaseLoader):
    """Class for loading basic study plans for HSE"""
    
    @property
    def _url(self) -> str:
        return HSE_BASIC_URL
    
    @property
    def _hyp_signature(self) -> str:
        return 'showBasicFaculty'
    
    # def load(path: str) -> None:
    #     __load_hse(HSE_BASIC_URL, 'showBasicFaculty', path, True)