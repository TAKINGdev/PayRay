![Alt Text](PayRay.png)
# 💳 Python Banking Application

A complete object-oriented banking system written in Python using `pandas` for data management and `customtkinter` for a modern graphical user interface (GUI).

## 🚀 Features

- 🧾 **User Registration & Deletion**
  - Sign up with first name, last name, username, and strong password
  - Delete existing user accounts

- 🔐 **User Login**
  - Authenticate using username and password
  - Prevents login if credentials are invalid

- 💰 **Banking Operations**
  - Deposit money
  - Withdraw funds
  - Transfer money to other accounts
  - View current account balance

- 🕓 **Transaction Logs**
  - All transactions are recorded with timestamps
  - Data is saved in `.csv` files

## 🧠 Tech Stack

- **Python 3.10+**
- **Pandas** for data handling
- **CustomTkinter** for modern GUI components
- **Object-Oriented Programming** structure

## 📁 Project Structure

BankingApp/
│
├── UserAccounts/
│ └── RegistrationedAccounts.csv
│
├── TransactionsUserAccount/
│ ├── TransactionsUserAccountHall.csv
│
├── UserRegistrationAndLogin.py
├── FinancialTransactions.py
├── main.py
└── README.md

markdown
Copy
Edit

- `UserRegistrationAndLogin.py`: Handles user registration, login verification, and deletion
- `FinancialTransactions.py`: Contains logic for deposit, withdrawal, balance inquiry, and transfer
- `main.py`: GUI logic using `customtkinter` for login and user dashboard
- CSV files store account data and balances

## 🧪 How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/banking-app.git
   cd banking-app
Install dependencies:

bash
Copy
Edit
pip install pandas customtkinter
Run the application:

bash
Copy
Edit
python main.py
✅ Requirements
Python 3.10 or newer

pandas

customtkinter

Note: customtkinter is a modern styled wrapper for tkinter. You can install it with pip install customtkinter.

🔒 Password Policy
To register an account, the password must:

Be at least 8 characters

Contain uppercase and lowercase letters

Include at least one digit

📦 Data Storage
All user and transaction data are stored locally in CSV files.

You can find these in the UserAccounts/ and TransactionsUserAccount/ directories.

📸 GUI Preview
Coming soon! (Or feel free to add screenshots here)

🛠 Future Enhancements
Add password hashing (e.g., with bcrypt)

Export transaction history as PDF

Multi-language support

Admin dashboard

Monthly account statement generation

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.
