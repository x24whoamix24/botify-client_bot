from marketplace_bot import MarketplaceBot


class FnacBot(MarketplaceBot):
    """
    Bots used to communicate with  https://www.fnac.com/ marketplace
    """
    def write_review(self, product_url, review):
        """
        Leaves a comment
        :param product_url: The product url
        :param review: The review to leave
        """

    def register(self):
        """
        Register to the Fnac service
        """
        pass