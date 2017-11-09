from pydci import *

class CleanTable(Context):
    class Waiter(StageProp):
        def clean_table(self):
            print("{} is cleaning the table".format(self.name))

    def __init__(self, waiter):
        self.Waiter = waiter

    def clean(self):
        self.Waiter.clean_table()


class WaitTable(Context):
    stuff = 'important stuff'

    class Waiter(Role):
        def wait_table(self):
            self.context.Apprentice.watch_and_learn()
            CleanTable(waiter=self).clean()
            print("{} waiting table".format(self.name))

    class Apprentice(StageProp):
        def watch_and_learn(self):
            print("{} started watching {}".format(self.name, self.context.Waiter.name))

    def __init__(self, waiter, apprentice):
        print('wait table init')
        self.Waiter = waiter
        self.Apprentice = apprentice

    def start(self, *args, **kwargs):
        self.Waiter.wait_table()


class Person(object):
    __slots__ = ['name']

    def __init__(self, name):
        self.name = name


p = Person('Vladi')
apprentice = Person('Jenny')
wt = WaitTable(p, apprentice)
wt.start()
