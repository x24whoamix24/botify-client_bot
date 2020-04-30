from Rakuten.rakuten_bot import RakutenBot

def main():
    bot = RakutenBot()
    bot.start_browser()
    bot.register()
    bot.leave_review("https://fr.shopping.rakuten.com/offer/buy/4865983651/masque-facial-jetable-ppe-avec-rapport-ce-ffp2-barre-de-nez-adaptable-masque-3-couches-masque-respirant-doux-tissu-non-tisse-boucle-d-oreille-bouche-masque-facial-protection-contre-la.html?bbaid=5951740877&xtatc=PUB-[PMC]-[H]-[HomePage]-[creme-de-la-creme]-[carrousel-tendance]-[4865983651]-[]", "wewe")

if (__name__ == "__main__"):
    main()