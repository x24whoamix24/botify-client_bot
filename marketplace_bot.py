import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import marketplace_bot_consts as consts

from captcha_solver.nocaptcha import CapatchaSolver
from comment_generator import CommentGenerator


class MarketplaceBot(object):
    """
    A General design for a bot used to communicate with a marketplace
    """

    def __init__(self):
        """
        Initializes the class variables
        """
        self.logged_in = False
        self.driver = None
        self.mail = ""
        self.firstname = ""
        self.lastname = ""

    def solve_captcha(self):
        """
        Verifies the bot by solving the website's captcha
        """
        # Switch to the Captcha's iframe
        captcha = CapatchaSolver(self.driver)
        while True:
            self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
            captcha.solve_captcha()
            # Check if we passed the captcha part by checking the page title
            wait = WebDriverWait(self.driver, 10)
            try:
                wait.until_not(EC.title_is(consts.BLOCKED))
                break
            except TimeoutException:
                self.driver.refresh()

    def get_review(self, language):
        """
        Obtains a generic review for a product
        :param language: The language of the review to obtain
        :return: str: The review in the selected language
        """
        comment_generator = CommentGenerator(language)
        return comment_generator.generateComment()

    def get_review_title(self, language):
        """
        Obtains a generic title for a review for a product
        :param language: The language of the review to obtain
        :return: str: The review in the selected language
        """
        comment_generator = CommentGenerator(language)
        return comment_generator.generateTitle()

    def start_browser(self):
        """
        Start the bot browser
        """
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option('w3c', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features");
        options.add_argument("--disable-blink-features=AutomationControlled");

        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                          Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                          })
                        """
        })
        self.driver.execute_cdp_cmd("Network.enable", {})
        self.driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36	"}})

    def stop_browser(self):
        """
        Closes the bot browser
        """
        self.driver.quit()

    def leave_review(self, product_url, review, review_title):
        """
        Leaves a review in a product page
        :param product_url: the link to the product
        :param review: The review to place
        :param review_title: The title for the review
        """
        raise NotImplementedError

    def wait_for_page_change(self, current_page):
        """
        Wait for the current page to change
        :param current_page: The current page
        """
        WebDriverWait(self.driver, 5).until(EC.url_changes(current_page))

    def register(self):
        """
        Registers to the marketplace
        :param url:
        :return:
        """
        raise NotImplementedError

    def create_new_mail(self):
        """
        Creates a new mail account
        """
        self.driver.get(consts.TEMP_MAIL)
        soup = BeautifulSoup(self.driver.page_source)
        self.mail = soup.find(id="email_id").attrs["data-value"]

    def get_name(self):
        self.driver.get(consts.RANDOM_NAME_GENERATOR)

        while True:
            name = self.driver.find_elements_by_xpath('//*[@id="user_value"]')[0]

            name = name.text
            name_list = name.split(" ")
            if len(name_list) != 2:
                # no name generated yet,
                # wait for the page to load
                time.sleep(0.5)
                continue
            self.firstname = name_list[0]
            self.lastname = name_list[1]
            break

    def verify_mail(self):
        """
        Verify the mail sent to the mail service
        """
        raise NotImplementedError
