import random

from Rakuten.rakuten_bot import RakutenBot


def main():
    product_options= ["https://fr.shopping.rakuten.com/offer/buy/4928602214/hat-no-id.html",
                    "https://fr.shopping.rakuten.com/offer/buy/4928598486/controleur-de-manette-de-jeu-gamepad-sans-fil-bluetooth-avec-poignee-a-6-axes-pour-switch-pro-ns-switch-pro-gamepad-pour-switch-console.html"]
    print("Begin rape session")
    change_star_rating = 10
    star_rating_counter = 0
    stars = 5
    end = 600
    for i in range(end):
        try:
            if star_rating_counter == change_star_rating:
                stars = 4
                star_rating_counter = 0
            link = random.choice(product_options)
            bot = RakutenBot()
            bot.start_browser()
            language = "fr"
            review = bot.get_review(language)
            review_title = bot.get_review_title(language)
            bot.register()
            bot.leave_review(
                link,
                review_title,
                review,
                stars=stars)
            bot.stop_browser()
            star_rating_counter += 1
            stars = 5
            print("finished {} out of {}".format(i, end))
        except Exception as e:
            print(e)


if (__name__ == "__main__"):
    main()
