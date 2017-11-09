from pydci import Role, Context


class Account(object):
    def __init__(self, amount):
        print "Creating a new account with balance of " + str(amount)
        self.balance = amount
        super(Account, self).__init__()

    def decrease_balance(self, amount):
        print "Withdraw " + str(amount) + " from " + str(self)
        self.balance -= amount

    def increase_balance(self, amount):
        print("Deposit " + str(amount) + " in " + str(self))
        self.balance += amount


class TransferMoneyContext(Context):
    class MoneySource(Role):
        def transfer(self, amount):
            if self.balance >= amount:
                self.decrease_balance(amount)
                self.context.MoneySink.receive(amount)

    class MoneySink(Role):
        def receive(self, amount):
            self.increase_balance(amount)

    def __init__(self, source, sink):
        self.MoneySource = source
        self.MoneySink = sink

    def __call__(self, amount):
        self.MoneySource.transfer(amount)


if __name__ == '__main__':
    source = Account(1000)
    destination = Account(-200)
    transfer_money = TransferMoneyContext(source, destination)
    transfer_money(300)

    print(source.balance)
    print(destination.balance)
