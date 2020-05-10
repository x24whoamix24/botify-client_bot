import secrets
import string
import re
import time
import urllib.request
import xmltodict


from googletrans import Translator
from rakuten_seller.sheet_handler.sheet_handler import SheetHandler

from rakuten_seller.consts import *
from marketplace_bot import MarketplaceBot
from captcha_solver.actions import ActionChains_Fake


class RakutenSeller(MarketplaceBot):
    """
    Bots used to communicate with https://fr.shopping.rakuten.com/ marketplace as a seller
    """

    def __init__(
        self,
        user,
        token,
        language = "en"
        ):
        super().__init__()
        self.language = language
        self.translator = Translator()
        self.user =  user
        self.token = token
        
    def connectToSheet(
        self,
        sheet_name,
        config_folder,
        config_files):
        """
        connects to a certain sheet 
        :param sheet_name: sheets name
        :param config_folder: config folder with cradentials
        :param config_files: config files names of cradentials to use
        :return: 
        """
        self.sheet_handler = SheetHandler(sheet_name, config_folder, config_files)

    def importProduct(self, product_type, ali_url, product_id, rakuten_url, sheet_number):
        """
        import a product from aliexpress to rakuten 
        :param product_type: type of product to import
        :param ali_url: aliexpress product url
        :param rakuten_url: rakuten product url
        :return: 
        """
        if product_type == PRODUCT:
            return
        self.data = []
        self.sheet_number = sheet_number
        return {
            SPORT_PRODUCT:self.importSportProduct,
            PRODUCT:self.importProduct,
        }[product_type](ali_url, product_id, rakuten_url)

    def importSportProduct(self, ali_url, product_id, rakuten_url):
        """
        import a sport product from aliexpress to rakuten 
        :param ali_url: aliexpress product url
        :param rakuten_url: rakuten product url
        :return: 
        """
        self.getSportData(ali_url, product_id, rakuten_url)
        self.writeData()

    def getSportData(self, ali_url, product_id, rakuten_url):
        ali_data = self.getAliexpressProductInfo(ali_url)
        rakuten_data =self.getRakutenProductInfo(product_id, rakuten_url)

        barcode = rakuten_data[BARCODE]
        sku = rakuten_data[SKU]
        type_of_sport = rakuten_data[TYPE_OF_SPORT]
        type_of_product = rakuten_data[TYPE_OF_PRODUCT]
        title = rakuten_data[TITLE]
        short_description = rakuten_data[SHORT_DESCRIPTION]
        brand = rakuten_data[BRAND]
        price = ali_data[PRICE]
        condition = "N"
        quantity = "100"
        custom_desc = ali_data[CUSTOM_DESC]
        advert_comment = ''
        main_picture = ali_data[MAIN_PICTURE]
        pic2 = ali_data[PIC2]
        pic3 = ali_data[PIC2]
        ship_by_rakuten = "0"
        shipping = "[@mode:RECOMMANDE@auth:1@lead:10@follow:0]"
        data = []
        for i in range(CELL_NUMBER):
            data.append(BLANK)
        
        data[SPORT_BARCODE] = barcode
        data[SPORT_SKU] = sku
        data[SPORT_TYPE_OF_SPORT] = type_of_sport
        data[SPORT_TYPE_OF_PRODUCT] = type_of_product
        data[SPORT_TITLE] = title
        if short_description == '' : 
            data[SPORT_SHORT_DESCRIPTION] = custom_desc
        else:
            data[SPORT_SHORT_DESCRIPTION] = short_description
        data[SPORT_BRAND] = brand
        data[SPORT_PRICE] = price
        data[SPORT_CONDISION] = condition
        data[SPORT_QUANTITY] = quantity
        data[SPORT_CUSTOM_DESC] = custom_desc
        data[SPORT_ADVERT_COMMENT] = advert_comment
        data[SPORT_MAIN_PICTURE] = main_picture
        data[SPORT_PIC2] = pic2
        data[SPORT_PIC3] = pic3
        data[SPORT_SHIP_BY_RAKUTEN] = ship_by_rakuten
        data[SPORT_SHIPPING_FRANCE] = shipping
        data[SPORT_SHIPPING_OVERSEAS] = shipping
        data[SPORT_SHIPPING_EUROPE] = shipping
        data[SPORT_SHIPPING_WORLD] = shipping

        self.data = data


    def getMainImageUrl(self):
        return self.driver.find_element_by_xpath("//img[@class='magnifier-image']").get_attribute('src')
    
    def getPicUrl(self,pic_number):
        self.driver.find_element_by_xpath("//ul[@class='images-view-list']/li[{}]".format(pic_number)).click()
        return self.getMainImageUrl()
    
    def getAliexpressProductInfo(self, ali_url):
        self.openAli(ali_url)
        time.sleep(3)
        self.setAliexpress("france", "fr", "EUR")
        self.scrollPage()
        
        price = self.getAliPrice() * PRICE_MARGINE
        custom_desc = self.driver.find_element_by_xpath("//div[@id='product-description']").get_attribute('innerHTML')
        main_picture = self.getMainImageUrl()
        pic2 = self.getPicUrl(2)
        pic3 = self.getPicUrl(3)

        return{
            PRICE:price,
            CUSTOM_DESC:custom_desc,
            MAIN_PICTURE:main_picture,
            PIC2:pic2,
            PIC2:pic3
        }


    def removePromo(self):
        try:
            self.driver.find_element_by_xpath("//a[@class='next-dialog-close']").click()
        except Exception as e:
            pass

    def setAliexpress(self, contry, language, currency):

        self.driver.find_element_by_xpath("//a[@id='switcher-info']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//a[@data-role='country']").click()
        self.driver.find_element_by_xpath("//div[@class='filter-list-container']/input").send_keys(contry)
        self.driver.find_element_by_xpath("//li[@data-code='fr']").click()

        self.driver.find_element_by_xpath("//span[@data-role='language-input']").click()
        self.driver.find_element_by_xpath("//input[@class='search-currency']").click()
        self.driver.find_element_by_xpath("//div[@class='search-container']/input").send_keys(language)
        self.driver.find_element_by_xpath("//a[@data-locale='fr_FR']").click()
        
        self.driver.find_element_by_xpath("//div[@data-role='switch-currency']").click()
        self.driver.find_element_by_xpath("//div[@class='switcher-currency item util-clearfix']//input").send_keys(currency)
        self.driver.find_element_by_xpath("//a[@data-currency='EUR']").click()
        self.driver.find_element_by_xpath("//button[@data-role='save']").click()
        
        time.sleep(10)

        self.removePromo()

    def openAli(self, url):
        self.driver.get(url)
        time.sleep(3)
        self.removePromo()
    
    def scrollPage(self):

        self.driver.execute_script("window.scrollTo(0, (document.body.scrollHeight * 0.2));")
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
    
    def getAliPrice(self):        
        price_text = self.driver.find_element_by_xpath("//span[@class='product-price-value']").text
        price = 0.0

        for token in re.split('\€ | - ', price_text):

            if ',' in token:
                token = token.replace(',','.')     
            try:
                token = float(token)
            except Exception as e:
                continue
            if price < token:
                price = token
        return price
        
    #old selenium implementation
    # def getRakutenProductInfo(self, rakuten_url):
    #     self.driver.get(rakuten_url)
        
    #     type_of_sport = self.driver.find_element_by_xpath("//div[@class='gsRow spacerBottomM']//li[1]//span").text
    #     type_of_product = self.driver.find_element_by_xpath("//div[@id='gsRow spacerBottomM']//li[2]//span").text
    #     title = self.driver.find_element_by_xpath("//div[@id='prdTitleBlock']/h1/span").text
    #     short_description = self.driver.find_element_by_xpath("//p[@class='description']").text
    #     brand = self.driver.find_element_by_xpath("//div[@id='prdTitleBlock']/span[@class='normal prdTitleBrand']/a").text

    #     return{
    #         TYPE_OF_SPORT: type_of_sport,
    #         TYPE_OF_PRODUCT: type_of_product,
    #         TITLE: title, 
    #         SHORT_DESCRIPTION: short_description, 
    #         BRAND: brand
    #     }

    def getRakutenProductInfo(self, product_id, rakuten_url):
        url = "https://ws.fr.shopping.rakuten.com/listing_ssl_ws?action=listing&login={}&pwd={}&version=2018-06-28&productids={}".format(self.user, self.token, product_id)
        file = urllib.request.urlopen(url)
        data = file.read()
        file.close()

        data = xmltodict.parse(data)

        type_of_sport = data['listingresult']['response']['products']['product']['category'].split('_',1)[1].replace('-',' ')
        type_of_product = data['listingresult']['response']['products']['product']['topic']
        title = data['listingresult']['response']['products']['product']['headline']
        brand = data['listingresult']['response']['products']['product']['caption']
        barcode = data['listingresult']['response']['products']['product']['references']['barcode']
        sku = barcode
        
        # self.driver.get(rakuten_url)
        # short_description = self.driver.find_element_by_xpath("//p[@class='description']").text
        short_description = ''
        return {
            BARCODE:barcode,
            SKU:sku,
            TYPE_OF_SPORT: type_of_sport,
            TYPE_OF_PRODUCT: type_of_product,
            TITLE: title, 
            SHORT_DESCRIPTION: short_description, 
            BRAND: brand
        }



    def writeData(self):
        self.sheet_handler.writeToSheet(self.sheet_number, self.data)
        

    def _translate(self, payload):
        """
        translates payload to a given comment
        :return: str: translated payload
        """
        return self.translator.translate(payload, dest=self.language).text






