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
            self.wait_for_clients_to_finish()
            print("{} waiting table".format(self.name))

        def wait_for_clients_to_finish(self):
            CleanTable(waiter=self).clean()

    class Apprentice(StageProp):
        def watch_and_learn(self):
            print("{} started watching {}".format(self.name, self.context.Waiter.name))

    def __init__(self, waiter, apprentice):
        self.Waiter = waiter
        self.Apprentice = apprentice

    def start(self, *args, **kwargs):
        self.Waiter.wait_table()


class Person(object):
    __slots__ = ['name']

    def __init__(self, name):
        self.name = name


p = Person('Bob')
apprentice = Person('Alice')
wt = WaitTable(p, apprentice)
wt.start()
