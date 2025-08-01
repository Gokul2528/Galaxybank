import random
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload
from Banking.db_layer.db_config import sessionLocal
from Banking.db_layer.model import UserLogin, Account, Transaction, ManagePayee, Loan


def signup(username, password, balance, mpin):
    session = sessionLocal()
    try:
        existing = session.query(UserLogin).filter_by(username=username).first()
        if existing:
            print("Username already exists.")
            return None

        user = UserLogin(username=username, password=password)
        session.add(user)
        session.flush()

        acctno = random.randint(10000, 99999)
        account = Account(acctno=acctno, balance=balance, mpin=mpin, userid=user.userid)
        session.add(account)
        session.commit()

        print(f"Account created successfully! Your account number is: {acctno}")
        return user
    except Exception as e:
        session.rollback()
        print("Error during signup:", e)
    finally:
        session.close()


def login(username, password):
    session = sessionLocal()
    try:
        user = session.query(UserLogin) \
                      .options(joinedload(UserLogin.account)) \
                      .filter_by(username=username, password=password) \
                      .first()
        if user:
            print(f"Welcome, {username}!")
        else:
            print("Invalid credentials.")
        return user
    finally:
        session.close()


def deposit(acctno, amount, mpin):
    session = sessionLocal()
    try:
        account = session.query(Account).filter_by(acctno=acctno, mpin=mpin).first()
        if not account:
            print("Invalid MPIN or account.")
            return
        account.balance += amount
        txn = Transaction(acctno=acctno, type="deposit", amount=amount)
        session.add(txn)
        session.commit()
        print("Deposit successful. Balance:", account.balance)
    except Exception as e:
        session.rollback()
        print("Deposit error:", e)
    finally:
        session.close()


def withdraw(acctno, amount, mpin):
    session = sessionLocal()
    try:
        account = session.query(Account).filter_by(acctno=acctno, mpin=mpin).first()
        if not account:
            print("Invalid MPIN or account.")
            return
        if account.balance < amount:
            print("Insufficient balance.")
            return
        account.balance -= amount
        txn = Transaction(acctno=acctno, type="withdraw", amount=amount)
        session.add(txn)
        session.commit()
        print("Withdrawal successful. Balance:", account.balance)
    except Exception as e:
        session.rollback()
        print("Withdraw error:", e)
    finally:
        session.close()


def view_balance(acctno, mpin):
    session = sessionLocal()
    try:
        account = session.query(Account).filter_by(acctno=acctno, mpin=mpin).first()
        if account:
            print("Your current balance is:", account.balance)
        else:
            print("Invalid MPIN or account.")
    finally:
        session.close()


def view_transaction_history(acctno):
    session = sessionLocal()
    try:
        transactions = session.query(Transaction).filter(Transaction.acctno == acctno).order_by(Transaction.timestamp.desc()).all()
        if not transactions:
            print("No transactions found.")
        else:
            print("Transaction History:")
            for txn in transactions:
                target = f" -> {txn.target_acct}" if txn.target_acct else ""
                print(f"{txn.timestamp} | {txn.type.title()} | ₹{txn.amount}{target}")
    finally:
        session.close()


def add_payee(owner_acct, payee_acct):
    session = sessionLocal()
    try:
        if not session.query(Account).filter_by(acctno=payee_acct).first():
            print("Payee account does not exist.")
            return
        if session.query(ManagePayee).filter_by(owner_acct=owner_acct, payee_acct=payee_acct).first():
            print("Payee already exists.")
            return
        session.add(ManagePayee(owner_acct=owner_acct, payee_acct=payee_acct))
        session.commit()
        print("Payee added successfully.")
    finally:
        session.close()


def fund_transfer(from_acct, to_acct, amount, mpin):
    session = sessionLocal()
    try:
        sender = session.query(Account).filter_by(acctno=from_acct, mpin=mpin).first()
        receiver = session.query(Account).filter_by(acctno=to_acct).first()
        if not sender or not receiver:
            print("Invalid account or MPIN.")
            return
        if sender.balance < amount:
            print("Insufficient balance.")
            return
        if not session.query(ManagePayee).filter_by(owner_acct=from_acct, payee_acct=to_acct).first():
            print("Payee not added. Add as payee first.")
            return
        sender.balance -= amount
        receiver.balance += amount
        session.add(Transaction(acctno=from_acct, type="transfer", amount=amount, target_acct=to_acct))
        session.commit()
        print(f"₹{amount} transferred to account {to_acct}.")
    except Exception as e:
        session.rollback()
        print("Transfer error:", e)
    finally:
        session.close()


def change_mpin(acctno, old_mpin, new_mpin):
    session = sessionLocal()
    try:
        account = session.query(Account).filter_by(acctno=acctno, mpin=old_mpin).first()
        if not account:
            print("Incorrect old MPIN.")
            return
        account.mpin = new_mpin
        session.commit()
        print("MPIN updated successfully!")
    finally:
        session.close()


def apply_loan(acctno, loan_type, amount, interest, duration_months):
    session = sessionLocal()
    try:
        account = session.query(Account).filter_by(acctno=acctno).first()
        if not account:
            print("Account not found.")
            return
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=30 * duration_months)
        loan = Loan(acctno=acctno, loan_type=loan_type, amount=amount, interest=interest,
                    start_date=start_date, end_date=end_date, status="Pending")
        session.add(loan)
        session.commit()
        print("Loan request submitted! Our bank will reach out to you soon.")
    finally:
        session.close()


def view_loans(acctno):
    session = sessionLocal()
    try:
        loans = session.query(Loan).filter_by(acctno=acctno).all()
        if not loans:
            print("No loan requests found.")
        else:
            for loan in loans:
                print(f"{loan.loan_type} | ₹{loan.amount} | Status: {loan.status} | Ends: {loan.end_date.date()}")
    finally:
        session.close()
