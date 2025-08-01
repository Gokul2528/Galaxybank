from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class UserLogin(Base):
    __tablename__ = "user_login"

    userid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    account = relationship("Account", back_populates="user", uselist=False)


class Account(Base):
    __tablename__ = "accounts"

    acctno = Column(Integer, primary_key=True)  # 5-digit random
    balance = Column(Float, nullable=False)
    mpin = Column(Integer, nullable=False)

    userid = Column(Integer, ForeignKey("user_login.userid"), unique=True, nullable=False)
    user = relationship("UserLogin", back_populates="account")
    transactions = relationship("Transaction", back_populates="account")
    payees = relationship("ManagePayee", back_populates="owner")
    loans = relationship("Loan", back_populates="account")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    acctno = Column(Integer, ForeignKey("accounts.acctno"))
    type = Column(String, nullable=False)  # deposit / withdraw / transfer
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    target_acct = Column(Integer, nullable=True)  # For transfers

    account = relationship("Account", back_populates="transactions")


class ManagePayee(Base):
    __tablename__ = "manage_payee"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_acct = Column(Integer, ForeignKey("accounts.acctno"))
    payee_acct = Column(Integer, nullable=False)

    owner = relationship("Account", back_populates="payees")


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    acctno = Column(Integer, ForeignKey("accounts.acctno"))
    loan_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    interest = Column(Float, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=False)
    status = Column(String, default="Pending")  # Always pending

    account = relationship("Account", back_populates="loans")
