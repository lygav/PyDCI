from pydci import Context, Role, StageProp

from models import *


class CheckOutBook(Context):
    class BookScanner(Role):

        def scan(self):
            another = True
            while another:
                self.BookScanner.scan_current_book()
                another = True if int(raw_input('Scan another?')) == 1 else False
            print("\r\n".join(map(lambda x: str(x), self.BookScanner.scanned_items)))

        def scan_current_book(self):
            book = self.scan()
            if book in self.scanned_items:
                print('{} Book already scanned'.format(book.name))
            else:
                self.scanned_items.append(book)

    def __init__(self, book_scanner):

        self.BookScanner = book_scanner

    def start(self):
        pass


class LibraryMembershipApplication(Context):
    class Guide(StageProp):
        def welcome(self):
            self.context.Output.add_line("Hello dear applicant.")
            self.context.Output.add_line("To apply for library membership please complete the registration.")

            self.context.Application.fill_details()
            self.context.Output.add_line("Thank you, your registration is complete!")

    class Application(StageProp):

        def fill_details(self):
            name = self.fill_name()
            password = self.fill_password(3)
            self.context.MembersRepository.process_application(name, password)

        def fill_name(self):
            name = self.context.Keypad.read_string('Please enter your name:')
            if len(name) <= 1:
                self.context.Output.add_line('Please enter a valid name.')
                self.fill_name()
            self.context.Output.add_line('Hello ' + name)
            return name

        def fill_password(self, attempts):
            password = self.context.Keypad.read_string('Please choose password:')
            if attempts <= 0:
                self.context.Output.add_line('Max attempts to enter password.')
                exit('Aborting registration...')
            elif len(password) < 3:
                self.context.Output.add_line('Password must be more than 3 chars')
                self.fill_password(attempts - 1)
            return password

    class MembersRepository(StageProp):

        def process_application(self, name, passsword):
            self.execute('''
            INSERT INTO members (name) VALUES (?)
            ''',
                         name)
            self.execute('''
            INSERT INTO membership (id, member_id, password) VALUES (?, ?, ?)
            ''',
                         self.context.MembershipIdProvider.new_id(),
                         self.cursor.lastrowid,
                         passsword)
            self.commit()

    class Keypad(StageProp):

        def read_string(self, prompt=None):
            return str(raw_input('{}\r\n'.format(prompt)))

    class Output(StageProp):

        def add_line(self, line):
            print(line)

    class MembershipIdProvider(StageProp):
        def new_id(self):
            import random
            return random.randrange(1000, 100000)

    def __init__(self, members_repository):
        self.MembersRepository = members_repository
        self.MembershipIdProvider = None
        self.Guide = None
        self.Application = None
        self.Keypad = None
        self.Output = None

    def start(self):
        return self.Guide.welcome()


print(LibraryMembershipApplication(
    SqliteDB('library.db')
).start())
