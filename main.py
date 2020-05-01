import random
import signal
import time
from contextlib import contextmanager

from Rakuten.rakuten_bot import RakutenBot


class TimeOutException(Exception):
    pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


class TimeoutException(Exception): pass


def bot_run(star_rating_counter, change_star_rating, product_options, stars):
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
    except Exception as e:
        if (bot):
            bot.stop_browser()
        print(e)


def main():
    product_options = ["https://fr.shopping.rakuten.com/offer/buy/4928602214/hat-no-id.html",
                       "https://fr.shopping.rakuten.com/offer/buy/4928598486/controleur-de-manette-de-jeu-gamepad-sans-fil-bluetooth-avec-poignee-a-6-axes-pour-switch-pro-ns-switch-pro-gamepad-pour-switch-console.html"]
    print("Begin rape session")
    change_star_rating = 10
    star_rating_counter = 0
    stars = 5
    end = 550
    # Setup signal for timeout on bot run
    for i in range(end):
        # Send signal after 5 minutes, this limits the bot run to max 5 minutes
        with time_limit(60 * 4):
            bot_run(star_rating_counter, change_star_rating, product_options, stars)
        print("finished {} out of {}".format(i, end))

if (__name__ == "__main__"):
    main()
