from Rakuten.rakuten_bot import RakutenBot

def main():
    bot = RakutenBot()
    bot.start_browser()
    review = bot.get_review("fr")
    bot.register()
    bot.leave_review("https://fr.shopping.rakuten.com/offer/buy/826153695/la-guerre-secrete-contre-les-peuples-de-claire-severac.html", review)
if (__name__ == "__main__"):
    main()