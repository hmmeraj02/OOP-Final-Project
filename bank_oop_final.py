import random


class Account():
    accounts = []

    def __init__(self, name, accountNum, email, address, acctype) -> None:
        self.name = name
        self.accountNum = accountNum
        self.email = email
        self.address = address
        self.acctype = acctype
        self.balance = 0
        self.transaction_history = []
        self.max_loan = 2
        self.take_loan = 0
        Account.accounts.append(self)

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            BankAdmin.total_balance += amount
            self.transaction_history.append(f"Deposited ${amount}")
            print(f"Deposited ${amount}. New balance: ${self.balance}")
        else:
            print("Invalid deposit")

    def withdraw(self, amount):
        result = BankAdmin.is_bankrupt
        # print(result)
        if result == True:
            print("Bank is bankrupt!")
            return
        if amount <= self.balance and amount > 0:
            self.balance -= amount
            BankAdmin.total_balance -= amount
            self.transaction_history.append(f"Withdrew ${amount}")
            print(f"Withdrew ${amount}. New balance: ${self.balance}")
        elif amount > self.balance:
            print("Withdrawal amount exceeded")
        else:
            print("Insufficient funds")

    def check_balance(self):
        print(f"Current Balance: ${self.balance}")

    def get_transaction_history(self):
        return self.transaction_history

    def get_loan(self, amount):
        result = BankAdmin.set_loan_status
        # print(result)
        if result == False:
            print("Loans are not currently available.")
            return
        if self.take_loan < self.max_loan:
            self.balance += amount
            BankAdmin.total_loan += amount
            self.transaction_history.append(f"Loan Deposited ${amount}")
            self.take_loan += 1
            print(
                f"Loan Deposited ${amount}. Loans taken so far: {self.take_loan}. New balance: ${self.balance}")
        else:
            print("Maximum loan limit reached.")

    def money_transfer(self, receiver_accountNum, amount):
        receiver = None
        for account in Account.accounts:
            if account.accountNum == receiver_accountNum:
                receiver = account
                break
        if receiver is not None:
            if amount <= self.balance and amount > 0:
                self.balance -= amount
                print(f"Account of {receiver.name}")
                receiver.deposit(amount)
                self.transaction_history.append(
                    f"Transferred {amount} to account number {receiver_accountNum}.")
                print('Transfer Completed Successfully')
        else:
            print("Account does not exist")


class SavingsAccount(Account):
    def __init__(self, name, accountNum, email, address) -> None:
        super().__init__(name, accountNum, email, address, "savings")


class CurrentAccount(Account):
    def __init__(self, name, accountNum, email, address) -> None:
        super().__init__(name, accountNum, email, address, "current")


class BankAdmin():
    total_balance = 0
    total_loan = 0
    # loan_status = True

    def create_account(self, name, accountNum, email, address, acctype):
        new_account = Account(name, accountNum, email, address, acctype)
        Account.accounts.append(new_account)

    def delete_account(self, del_accountNum):
        for account in Account.accounts:
            if account.accountNum == del_accountNum:
                Account.accounts.remove(account)
                return f"Account {del_accountNum} is deleted."
            return "No such account exists."

    def user_list(self):
        return Account.accounts

    def total_user_balance(self):
        for account in Account.accounts:
            self.total_balance += account.balance
            return f"Total Available Balance: ${self.total_balance}"

    def total_loan_taken(self):
        return f"Total Loan Amount: ${self.total_loan}"

    @classmethod
    def set_loan_status(self, status):
        self.set_loan_status = status

    @classmethod
    def is_bankrupt(self, status):
        self.is_bankrupt = status


currentUser = None
admin = ['Meraj', 12345]
while True:
    if currentUser == None:
        print("No user logged in!")
        ch = input("Register/Login (R/L): ")
        if ch == 'R':
            name = input("Name: ")
            accountNum = random.randint(1000, 1999)
            email = input("Email ID: ")
            address = input("Address: ")
            acctype = input("Savings Account or Current Account (sa/ca): ")
            if acctype == "sa":
                currentUser = SavingsAccount(
                    name, accountNum, email, address)
                print(f"<<<Account Number: {accountNum}>>>")
            else:
                currentUser = CurrentAccount(
                    name, accountNum, email, address)
                print(f"<<<Account Number: {accountNum}>>>")
        elif ch == 'L':
            print("1. Log in as User")
            print("2. Log in as Admin")
            op = int(input("Choose option (1/2): "))
            if op == 1:
                accNum = int(input("User's Account Number: "))
                for account in Account.accounts:
                    if account.accountNum == accNum:
                        currentUser = account
                        break
            elif op == 2:
                ch = int(input("Enter the Admin's password: "))
                if admin[1] == ch:
                    currentUser = BankAdmin()
                    print("Welcome Admin Panel!\n")
                    print("1. Create an account")
                    print("2. Delete an account")
                    print("3. Show list of all user accounts")
                    print("4. Check Total balance of all users")
                    print("5. Check Total amount of loans taken by the users")
                    print("6. Loan feature on or off")
                    print("7. Bankrupt")
                    print("8. Logout\n")
                    choice = int(input("Enter your choice: "))
                    if choice == 1:
                        name = input("Name: ")
                        accountNum = random.randint(1000, 1999)
                        email = input("Email ID: ")
                        address = input("Address: ")
                        acctype = input(
                            "Savings Account or Current Account (sa/ca): ")
                        if acctype == "sa":
                            newAcc = SavingsAccount(
                                name, accountNum, email, address)
                            print(f"<<<Account Number: {accountNum}>>>")
                        else:
                            newAcc = CurrentAccount(
                                name, accountNum, email, address)
                            print(f"<<<Account Number: {accountNum}>>>")
                    elif choice == 2:
                        accNum = int(input("Account Number to be deleted: "))
                        result = currentUser.delete_account(accNum)
                        print(result)
                    elif choice == 3:
                        accounts = currentUser.user_list()
                        for account in accounts:
                            print({account.name}, {account.accountNum})
                    elif choice == 4:
                        result = currentUser.total_user_balance()
                        print(result)
                    elif choice == 5:
                        result = currentUser.total_loan_taken()
                        print(result)
                    elif choice == 6:
                        status = input("Loan feature on or off (on/off): ")
                        if status == 'on':
                            currentUser.set_loan_status(True)
                        elif status == 'off':
                            currentUser.set_loan_status(False)
                        else:
                            print("Invalid option.")
                    elif choice == 7:
                        status = input("Bankrupt on or off (on/off): ")
                        if status == 'on':
                            currentUser.is_bankrupt(True)
                        elif status == 'off':
                            currentUser.is_bankrupt(False)
                        else:
                            print("Invalid option.")
                    elif choice == 8:
                        currentUser = None
                    else:
                        print("Invalid Option Chosen.\n")
                else:
                    print("Incorrect Password.")

    else:
        if isinstance(currentUser, Account):
            print(f"\nWelcome {currentUser.name}!")
            if currentUser.acctype == "savings" or currentUser.acctype == "current":
                print("1. Deposit")
                print("2. Withdrawal")
                print("3. Check Balance")
                print("4. Transaction History")
                print("5. Request for Loan")
                print("6. Transfer Money")
                print("7. Logout\n")
                op = int(input("Choose Option: "))
                if op == 1:
                    amount = int(input("\nEnter the deposit amount: $"))
                    currentUser.deposit(amount)
                elif op == 2:
                    amount = int(input("\nEnter the withdrawal amount: $"))
                    currentUser.withdraw(amount)
                elif op == 3:
                    currentUser.check_balance()
                elif op == 4:
                    transaction_history = currentUser.get_transaction_history()
                    print(transaction_history)
                elif op == 5:
                    loanAmount = int(
                        input("\nEnter the requested loan amount: $"))
                    currentUser.get_loan(loanAmount)
                elif op == 6:
                    recAccNum = int(
                        input("\nEnter recipient's account number: "))
                    amtToTransfer = int(input("\nEnter transfer amount: $"))
                    currentUser.money_transfer(recAccNum, amtToTransfer)
                elif op == 7:
                    currentUser = None
                else:
                    print("Invalid option chosen.")

        elif isinstance(currentUser, BankAdmin):
            print("Welcome Admin Panel!\n")
            print("1. Create an account")
            print("2. Delete an account")
            print("3. Show list of all user accounts")
            print("4. Check Total balance of all users")
            print("5. Check Total amount of loans taken by the users")
            print("6. Loan feature on or off")
            print("7. Bankrupt")
            print("8. Logout\n")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                name = input("Name: ")
                accountNum = random.randint(1000, 1999)
                email = input("Email ID: ")
                address = input("Address: ")
                acctype = input("Savings Account or Current Account (sa/ca): ")
                if acctype == "sa":
                    newAcc = SavingsAccount(
                        name, accountNum, email, address)
                    print(f"<<<Account Number: {accountNum}>>>")
                else:
                    newAcc = CurrentAccount(
                        name, accountNum, email, address)
                    print(f"<<<Account Number: {accountNum}>>>")
            elif choice == 2:
                accNum = int(input("Account Number to be deleted: "))
                result = currentUser.delete_account(accNum)
                print(result)
            elif choice == 3:
                accounts = currentUser.user_list()
                for account in accounts:
                    print({account.name}, {account.accountNum})
            elif choice == 4:
                result = currentUser.total_user_balance()
                print(result)
            elif choice == 5:
                result = currentUser.total_loan_taken()
                print(result)
            elif choice == 6:
                status = input("Loan feature on or off (on/off): ")
                if status == 'on':
                    currentUser.set_loan_status(True)
                elif status == 'off':
                    currentUser.set_loan_status(False)
                else:
                    print("Invalid option.")
            elif choice == 7:
                status = input("Bankrupt on or off (on/off): ")
                if status == 'on':
                    currentUser.is_bankrupt(True)
                elif status == 'off':
                    currentUser.is_bankrupt(False)
                else:
                    print("Invalid option.")
            elif choice == 8:
                currentUser = None
            else:
                print("Invalid Option Chosen.\n")
