import secrets
import string
import random

import Rakuten.consts as consts
from marketplace_bot import MarketplaceBot


class RakutenBot(MarketplaceBot):
    """
    Bots used to communicate with https://fr.shopping.rakuten.com/ marketplace
    """

    def __init__(self):
        super().__init__()

    def write_review(self, product_url, review):
        """
        Leaves a comment
        :param product_url: The product url
        :param review: The review to leave
        """

    def _fill_out_registration(self):
        """
        Fills out the registration form and registers
        """
        # Email
        email_field = self.driver.find_element_by_xpath('//*[@id="e_mail"]')
        email_field.send_keys(self.mail)
        # Confirm mail
        email_field = self.driver.find_element_by_xpath('//*[@id="e_mail2"]')
        email_field.send_keys(self.mail)

        # Generate and put password
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(20))  # for a 20-character password
        pass_field = self.driver.find_element_by_xpath('//*[@id="password"]')
        pass_field.send_keys(password)

        # Select gender
        choice = random.choice([True, False])
        if choice:
            # Male
            gender = self.driver.find_element_by_name('<span class="fld_lbl">Mr</span>')

        else:
            # Female
            gender = self.driver.find_element_by_name('<span class="fld_lbl">Mrs</span>')
        gender.click()

        day = random.randint(1, 30)
        month = random.randint(1, 12)
        year = random.randint(1950, 2000)
        self.driver.find_element_by_xpath('//*[@id="birth_day"]').send_keys(str(day))
        self.driver.find_element_by_xpath('//*[@id="birth_month"]').send_keys(str(month))
        self.driver.find_element_by_xpath('//*[@id="birth_year"]').send_keys(str(year))

        # Click on submit button
        self.driver.find_element_by_xpath('//*[@id="submit_btn2"]').click()

    def register(self):
        """
        Register to the Fnac service
        """
        self.create_new_mail()
        self.get_name()

        self.driver.get(consts.REGISTER_PAGE)
        if ("You have been blocked" in self.driver.page_source):
            self.solve_captcha()
        self.driver.get(consts.REGISTER_PAGE)

        # Click on registration button
        bt = self.driver.find_element_by_xpath('//*[@id="sbtn_register"]')
        bt.click()
        self._fill_out_registration()
