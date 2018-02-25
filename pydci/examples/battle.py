from pydci import *

def somefunc(player):
    player.say()

class Interview(Context):
    class Interviewee(Role):
        def say(self):
            print("[{}] {} Hello!".format(self.name, self.comms))

    class Battle(StageProp):

        @property
        def winner(self):
            return self.Bear

    class Interviewer(Role):
        def interview(self):
            print("[Interviewer] Hello Winner!")
            #should fail because you shouldn't call nested Contexts Roles
            self.context.Battle.winner.say()

    def __init__(self, interviewer, battle):
        self.Interviewer = interviewer
        self.Battle = battle

    def start(self):
        self.Interviewer.interview()


class Battle(Context):
    class Bear(Role):
        def say(self):
            print("{} [{}] Grrrrr.....".format(self.context.Game.id, self.name))

        def fight(self):
            self.say()
            self.context.Lion.fight()

    class Lion(Role):
        def say(self):
            print("{} [{}] Meow.....".format(self.context.Game.id, self.name))

        def fight(self):
            self.say()

    class Game(StageProp):
        @property
        def id(self):
            return self.gid

    def __init__(self, id, player1, player2):
        self.Game = id
        self.Bear = player1
        self.Lion = player2

    def start(self):
        print("Started battle of id {}".format(self.Game.id))
        self.Bear.fight()
        Interview(Player('Interviewer', 'says'), b1).start()
        somefunc(self.Bear)



class Player(object):
    def __init__(self, name, comms):
        self.name = name
        self.comms = comms

    def say(self):
        print('Game speaks')


class Game(object):
    def __init__(self, gid):
        self.gid = gid




player = Player(name='Jack', comms='says')
cpu = Player(name='Cyborg', comms='beleeps')
b1 = Battle(Game(1), player, cpu)
b2 = Battle(Game(2), cpu, player)
b3 = Battle(Game(3), cpu, cpu)
b1.start()
b2.start()
b3.start()

