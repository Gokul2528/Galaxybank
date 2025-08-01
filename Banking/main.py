from Banking.db_layer.db_config import engine
from Banking.db_layer.model import Base
from Banking.service.bankservice import (
    signup, login,
    deposit, withdraw, view_balance, view_transaction_history,
    add_payee, fund_transfer, change_mpin,
    apply_loan, view_loans
)

Base.metadata.create_all(bind=engine)

def main():
    print("=====Welcome to Galaxy Bank=====")

    user = None
    while True:
        print("\n--- Main Menu ---")
        print("1. Login")
        print("2. Signup (Open New Account)")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            user = login(username, password)
            if user:
                break

        elif choice == "2":
            username = input("Choose username: ")
            password = input("Choose password: ")
            balance = float(input("Initial deposit: "))
            mpin = int(input("Set 4-digit MPIN: "))
            signup(username, password, balance, mpin)

        elif choice == "3":
            print("Thank you for traveling with Galaxy Bank!")
            return

        else:
            print("Invalid choice. Please try again.")

    acctno = user.account.acctno
    while True:
        print("\n--- Galaxy Banking Menu ---")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. View Balance")
        print("4. Transaction History")
        print("5. Add Payee")
        print("6. Fund Transfer")
        print("7. Change MPIN")
        print("8. Apply for Loan")
        print("9. View Loan Requests")
        print("10. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            amt = float(input("Amount to deposit: "))
            mpin = int(input("Enter MPIN: "))
            deposit(acctno, amt, mpin)

        elif choice == "2":
            amt = float(input("Amount to withdraw: "))
            mpin = int(input("Enter MPIN: "))
            withdraw(acctno, amt, mpin)

        elif choice == "3":
            mpin = int(input("Enter MPIN: "))
            view_balance(acctno, mpin)

        elif choice == "4":
            view_transaction_history(acctno)

        elif choice == "5":
            payee = int(input("Enter payee account number: "))
            add_payee(acctno, payee)

        elif choice == "6":
            to_acc = int(input("Enter payee account number: "))
            amt = float(input("Amount to transfer: "))
            mpin = int(input("Enter MPIN: "))
            fund_transfer(acctno, to_acc, amt, mpin)

        elif choice == "7":
            old = int(input("Enter old MPIN: "))
            new = int(input("Enter new 4-digit MPIN: "))
            change_mpin(acctno, old, new)

        elif choice == "8":
            loan_type = input("Enter loan type (Home/Car/Personal): ")
            amount = float(input("Enter loan amount: "))
            interest = float(input("Enter interest rate %: "))
            duration = int(input("Duration in months: "))
            apply_loan(acctno, loan_type, amount, interest, duration)

        elif choice == "9":
            view_loans(acctno)

        elif choice == "10":
            print("Logging out... Thank you for flying with Galaxy Bank!")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()