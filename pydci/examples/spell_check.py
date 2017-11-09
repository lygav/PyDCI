from pydci import *


class SpellCheck(object):
    class CurrentSelection(Role):
        pass

    class SpellChecker(Role):
        pass

    class Dictionary(Role):
        pass

    def __init__(self, text, dictionary):
        self.CurrentSelection = SpellCheck.CurrentSelection(text)
        self.dictionary = dictionary


def WordList(object):
    def __init__(self, words):
        self.word_list = words


class Text(object):
    pass


