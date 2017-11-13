from pydci import *
import enchant
from StringIO import StringIO


class SpellCheck(Context):
    class CurrentSelection(Role):
        pass

    class SpellChecker(Role):

        def check(self):
            for word in self.context.CurrentSelection.read().split(" "):
                print("checking {}".format(word.strip()))
                if not super(SpellCheck.SpellChecker, self).check(word):
                    self.context.Ouput.write('The text has spelling errors \r\n')
                    suggestions = self.suggest(word)
                    if suggestions:
                        self.context.Ouput.write('Here are suggestions for `{}`: \r\n'.format(word.strip()))
                        self.context.Ouput.write('\r\n'.join(suggestions))

        def suggest(self, word):
            return super(SpellCheck.SpellChecker, self).suggest(word)

    class Ouput(Role):
        pass

    def __init__(self, text, dictionary, output):
        self.CurrentSelection = text
        self.SpellChecker = dictionary
        self.Ouput = output

    def check(self):
        self.SpellChecker.check()
        return self.Ouput


class TextBuffer(StringIO):
    pass


class LanguageDictionary(enchant.Dict):
    pass


text = """
Eye have a spelling chequer,
It came with my Pea Sea.
It plane lee marks four my revue
Miss Steaks I can knot sea.
"""

buff = TextBuffer(text)

dict = LanguageDictionary('en_US')

spell_check = SpellCheck(buff, dict, TextBuffer())
output = spell_check.check()
#print(output.read())



