import random
from googletrans import Translator

PRODUCT_QUALITY = [
    "The product's quality was very high. ",
    "The product is great and as I wanted. ",
    "I love it! the best I can imagine. ",
    "Exactly as I wanted. Thank so much! ",
    "Every time I bring it out in public somebody makes a comment about how nice it is. ",
    "I'm so happy that I bougnt this. ",
    "Love the colour and quality of the product. ",
    "The quality of this qulity is so good, i use it all the time! ",
    "I use this every time i get the chance! Recommend highly to everybody. ",
    "I just adore it! I recommend it to almost everyboy i know. "
]
SELLER_QUALITY = [
    "The seller is very responsive and understanding. ",
    "Thank you so much for the responsiveness and understanding. ",
    "Seller is super reliable and nice. ",
    "One of the best seller I have ever Bought from. Recommended! ",
    "I had some problem finding the product. The seller was so helpful, i so glad i bought here! "
]
SHIPPING_QUALITY = [
    "The product's quality was very high. ",
    "Shipping tracking was accurate and very useful. ",
    "Shipping was very compitant and hasty. ",
    "Got the product intacte and no harm gotten to it. ",
    "Quality of shipment was of the highest thanks to seller. ",
]
SHIPPING_TIME = [
    "The shipping was very fast. ",
    "The shipping was as promised. "
    "Shipment Exactly as specifed. "
]

COMMENT_DATA = [PRODUCT_QUALITY, SHIPPING_QUALITY, SELLER_QUALITY, SHIPPING_TIME]
TITLES = [
             "It saved my life",
             "Better then my wife",
             "THIS IS THE BEST",
             "I just love it",
             "I use it everyday"
             "just love it",
             "traded my pig for this",
             "Don't kill, buy this",
             "SUPER good!!!",
             "I love it",
             "How didn't i got this before"
         ] + PRODUCT_QUALITY


class CommentGenerator(object):
    """docstring for CommentGenerator"""

    def __init__(
            self,
            language="en"
    ):
        super(CommentGenerator, self).__init__()

        self.language = language
        self.translator = Translator()

    def generateComment(self):
        comment = ""
        for sentence in COMMENT_DATA:
            comment += sentence[random.randint(0, len(sentence) - 1)]

        return self.translate(comment)

    def generateTitle(self):
        return self.translate(TITLES[random.randint(0, len(TITLES) - 1)])

    def translate(self, comment):
        return self.translator.translate(comment, dest=self.language).text
