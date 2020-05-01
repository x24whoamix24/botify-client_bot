import time
import random
import string
import secrets

from Fnac import consts
from captcha_solver.actions import ActionChains_Fake
from marketplace_bot import MarketplaceBot


class FnacBot(MarketplaceBot):
    """
    Bots used to communicate with  https://www.fnac.com/ marketplace
    """

    def leave_review(self, product_url, review_title, review, stars=5):
        """
        Leave a review on a product
        :param product_url: The product url
        :param review_title: The title for the review
        :param review: The review to leave
        :param stars: Amount of stars the product receives
        """
        self.driver.get(product_url)
        time.sleep(2)
        # Click on review option
        self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]'
                                          '/section[1]/div[2]/div[1]/span/span[1]').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/section[1]'
                                          '/div[2]/div[1]/span/span[3]/div/div[2]/div/a').click()

        time.sleep(2.5)

        # Give stars to the product
        # Select the star element
        stars_element = self.driver.find_element_by_xpath("//*[(text()='Donner un avis')]").click()
        time.sleep(1)

        # Give star rating
        self.driver.find_element_by_xpath('//*[@id="star{}"]/label'.format(stars)).click()

        # Write review title
        self.driver.find_element_by_xpath('//*[@id="Review_Title"]').send_keys(review_title)

        # Write review content
        self.driver.find_element_by_xpath('//*[@id="Review_Text"]').send_keys(review)


        # Submit review
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.driver.find_element_by_xpath('//*[@id="btnSubmit"]').click()
        # Watt after submitting review
        time.sleep(consts.WAIT_AFTER_REVIEW_TIME)

    def _fill_out_registration(self):
        # Select gender
        choice = random.choice([True, False])
        if choice:
            # Male
            gender = self.driver.find_element_by_xpath("//*[(text()='Monsieur')]")

        else:
            # Female
            gender = self.driver.find_element_by_xpath("//*[(text()='Madame')]")
        gender.click()
        # Fill out last name
        self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div[1]/div[1]/div[1]'
                                          '/form/div[2]/div[1]/div/div/div/div/input').send_keys(self.lastname)
        # Fill out first name
        self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div[1]/div[1]/div[1]/'
                                          'form/div[2]/div[2]/div/div/div/div/input').send_keys(self.firstname)
        # Fill out email
        self.driver.find_element_by_xpath('//*[@id="email"]').send_keys(self.mail)
        # Confirm address

        # Fill out password

        password = ''.join(secrets.choice(string.digits) for i in range(4))
        password += ''.join(secrets.choice(string.ascii_lowercase) for i in range(4))
        password += ''.join(secrets.choice(string.punctuation) for i in range(4))
        password += ''.join(secrets.choice(string.ascii_uppercase) for i in range(4))

        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
        # Press create account button
        self.driver.find_element_by_class_name("button__signup").click()
        time.sleep(2.5)
        # Confirm that our Email address is legit
        self.driver.find_element_by_xpath("//*[contains(text(), 'confirme que mon adresse est correcte')]").click()
        time.sleep(2.5)
        # Scroll down to button
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.driver.find_element_by_class_name("button__signup").click()

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
        self._fill_out_registration()
        time.sleep(3)
        self.driver.find_element_by_xpath("//*[contains(text(), 'Passer cette')]").click()