import os
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from config.urls import urls
from config.elements import elements
from config.semrush import user
from service.final_report import FinalReport
from service.overview_slicer import OverviewSlicer
import random


class AbstractSelenium:
    def __init__(self):
        self.__init_browser()
        self.__login()
        self.__login_error()
        self.__reffering = ""
        self.__report = FinalReport()

    def __set_browser_options(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        return firefox_options

    def __set_browser_preferences(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.dir', os.getcwd())
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
        profile.update_preferences()
        return profile

    def __init_browser(self):
        self.browser = webdriver.Firefox(firefox_options=self.__set_browser_options(),
                                         firefox_profile=self.__set_browser_preferences())

    def __login_error(self):
        try:
            time.sleep(5)
            self.browser.find_element_by_xpath(elements['error_login_btn']).click()
            self.browser.find_element_by_xpath(elements['error_login_user']).send_keys(user['user'])
            self.browser.find_element_by_xpath(elements['error_login_pwd']).send_keys(user['pwd'])
            self.browser.find_element_by_xpath(elements['error_login_submit']).click()
        except NoSuchElementException:
            pass

    def __login(self):
        self.browser.get(urls['login'])
        self.browser.find_element_by_xpath(elements['login_user']).send_keys(user['user'])
        self.browser.find_element_by_xpath(elements['login_pwd']).send_keys(user['pwd'])
        self.browser.find_element_by_xpath(elements['login_submit']).click()

    def __search_domain(self, domain):
        self.browser.get(urls['search'].format(domain))

    def __extract_anchors(self, domain):
        print("Extract top 3 anchors...")
        time.sleep(2)
        self.browser.get(urls['anchors'].format(domain))
        self.__anchors = []
        for i in range(1, 4):
            try:
                self.__anchors.append(self.browser.find_element_by_xpath(elements['anchor'].format(str(i))).text)
            except NoSuchElementException:
                self.__anchors.append(" ")
        print("Finsh")

    def __extract_referring(self, domain):
        print("Extract reffering domains...")
        self.browser.get(urls['refdomains'].format(domain))
        time.sleep(2)
        try:
            self.__reffering = self.browser.find_element_by_xpath(elements['ref_domains']).text
        except NoSuchElementException:
            print("No reffering domains...")
            self.__reffering = 0
        print("Finish")

    def __peaks_csv_download(self, domain):
        print("Download file with peaks")
        self.__search_domain(domain)
        try:
            if self.browser.find_element_by_xpath(elements['no_data']).text == 'We have no data to show':
                self.__no_data_found = True
                print("No data found")
        except NoSuchElementException:
            self.browser.implicitly_wait(10)
            self.browser.find_element_by_xpath(elements['filter_all_time']).click()
            self.browser.find_element_by_xpath(elements['btn_export']).click()
            self.browser.find_element_by_xpath(elements['btn_csv']).click()
            time.sleep(5)
        print("Download complete")

    def __extrac_process(self, domain):
        self.__no_data_found = False
        error = True
        while error is True:
            try:
                domain = domain.strip('\n')
                print("Starting extraction process for the domain ", domain)
                self.__peaks_csv_download(domain)
                self.__extract_anchors(domain)
                self.__extract_referring(domain)
                if self.__no_data_found is False:
                    over = OverviewSlicer()
                    peaks = over.peaks_list
                else:
                    peaks = ['No data', 'No Data', 'No Data', 'No Data']
                print("Successful extraction process")
                print("Writing another line in the report\n")
                self.__report.new_line(domain, self.__reffering, peaks[3], peaks[2], peaks[1], peaks[0],
                                       self.__anchors[0], self.__anchors[1], self.__anchors[2])
                error = False
                time.sleep(random.randint(20, 60))
            except Exception as err:
                print('An error was found, redoing the domain ', domain, '\n', err)
                time.sleep(10)

    def start(self):
        for files in os.listdir(os.path.join(os.getcwd(), "upload")):
            path = os.path.join(os.getcwd(), "upload", files)
            if path.endswith(".txt"):
                with open(path, 'r', encoding='utf-16') as file:
                    for domain in file:
                        self.__extrac_process(domain)
                os.remove(path)
            elif path.endswith(".csv"):
                with open(path, 'r') as file:
                    for domain in file:
                        self.__extrac_process(domain)
                os.remove(path)
