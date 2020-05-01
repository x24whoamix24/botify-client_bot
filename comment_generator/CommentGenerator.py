import random
from googletrans import Translator

from comment_generator.consts import *


class CommentGenerator(object):
    """Comment generator for reviews in marketplace sites"""

    def __init__(
            self,
            language="en"
    ):
        self.language = language
        self.translator = Translator()

    def generateComment(self):
        """
        Generates review comment randomly
        :return: str: comment 
        """
        comment = ""
        for sentence in COMMENT_DATA:
            comment += sentence[random.randint(0, len(sentence) - 1)]

        return self._translate(comment)

    def generateTitle(self):
        """
        Generates review title randomly
        :return: str: title 
        """
        return self._translate(TITLES[random.randint(0, len(TITLES) - 1)])

    def _translate(self, payload):
        """
        translates payload to a given comment
        :return: str: translated payload
        """
        return self.translator.translate(payload, dest=self.language).text
