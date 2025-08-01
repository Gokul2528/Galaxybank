Project Title:Galaxy Bank

Description:
Galaxy Bank is a console-based banking management system that allows users to manage their accounts efficiently.
It supports essential banking operations like deposits, withdrawals, managing payees, and viewing transactions.

Features:
*User signup with random 5-digit account number
*Secure login using username and password
*Deposit and withdraw money
*View balance and transaction history
*Manage payees and transfer funds
*Change MPIN
*Request loan (status will be pending; manual verification required)

Installation
*Clone the repository:
      git clone https://github.com/Gokul2528/Galaxybank.git
      cd Galaxybank
*Install required dependencies:
     pip install -r requirements.txt
*Configure PostgreSQL in db_config.py if needed:
     engine = create_engine("postgresql+psycopg2://postgres:0000@localhost/bankdb")
*Run the application:
     python -m Banking.main

Tech Stack:
*Python 3
*SQLAlchemy ORM
*PostgreSQL
*psycopg2-binary

Note
This project was initially suggested to be implemented using JDBC.
I chose to implement it using Python with SQLAlchemy ORM because it reduces boilerplate code, improves maintainability, and allows rapid development while fully meeting the functional requirements
