import sqlite3


class User(object):
    def __init__(self, name):
        self.name = name


class Member(User):
    pass


class Membership(object):
    def __init__(self, member_id, id, password):
        self.member_id = member_id
        self.id = id
        self.password = password


class MemberRecord(object):
    def __init__(self, member_id):
        self.member_id = member_id




class Book(object):
    def __init__(self, title, author, accessionId):
        self.title = title
        self.author = author
        self.accessionId = accessionId

    def __str__(self):
        return "{} {}".format(self.title, self.accessionId)


class Scanner(object):
    def scan(self):
        pass


class CliScanner(Scanner):
    def __init__(self):
        self.scanned_items = list()

    def scan(self):
        import random
        name = str(raw_input('Enter Book Name: '))
        return Book(name, 'no author', "bk-{:.2}".format(random.random()))


class SqliteDB(object):

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    def execute(self, query, *params):
        self.cursor.execute(query, tuple(params))

    def commit(self):
        self.conn.commit()

    def close(self):
        self.close()
