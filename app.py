import os
from service.abstract_selenium import AbstractSelenium
from service.send_report import SendReport


class App:
    def __init__(self):
        browser = AbstractSelenium()
        browser.start()
        SendReport(os.path.join(os.getcwd(), "DOMAIN-report.xlsx"))
