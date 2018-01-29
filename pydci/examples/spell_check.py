from pydci import *
import enchant
from StringIO import StringIO


class SpellCheck(Context):
    class CurrentSelection(Role):
        pass

    class SpellChecker(Role):

        def do_spellckeck(self):
            for word in self.context.CurrentSelection.words():
                if not self.check(word):
                    self.context.Ouput.write('The text has spelling errors \r\n')
                    suggestions = self.suggest(word)
                    if suggestions:
                        self.context.Ouput.write('Here are suggestions for `{}`: \r\n'.format(word.strip()))
                        self.context.Ouput.write('-'.join(suggestions))


    class Ouput(Role):
        pass

    def __init__(self, text, dictionary, output):
        self.CurrentSelection = text
        self.SpellChecker = dictionary
        self.Ouput = output

    def check(self):
        self.SpellChecker.do_spellckeck()
        return self.Ouput


class TextBuffer(StringIO):

    def words(self):
        for line in self.readlines():
            if len(line) > 1:
                for word in line.strip().rstrip('.,-').split(" "):
                    yield word

        self.seek(0)


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

out = TextBuffer()
spell_check = SpellCheck(buff, dict, out)
spell_check.check()
out.seek(0)
print(out.read())


