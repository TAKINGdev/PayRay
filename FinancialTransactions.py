from datetime import datetime
import pandas as pd
import os

class Transactions:
    csvPath = 'TransactionsUserAccount/TransactionsUserAccountHall.csv'
    TrnsactionsCompile = ''
    RootMessage = 'root > FinancialTrnsactions'

    @classmethod
    def Deposit(cls, Username: str, amount: float):
        Hall = cls.LoadTrnsactionsHall()
        if amount <= 0:
            cls.TrnsactionsCompile = False, f'{cls.RootMessage} > Deposit -> invalid deposit amount'
            return

        if Username not in Hall['Username'].values:
            cls.TrnsactionsCompile = False, f'{cls.RootMessage} > Deposit -> username not found in transactions hall'
            return

        Hall.loc[Hall['Username'] == Username, ['Balance', 'Date']] = \
            Hall.loc[Hall['Username'] == Username].assign(
                Balance=lambda df: df['Balance'] + amount,
                Date=cls.GetDateTime()
            )
        Hall.to_csv(cls.csvPath, index=False)
        cls.TrnsactionsCompile = True, f'{cls.RootMessage} > Deposit -> deposit of {amount} successful'

    @classmethod
    def Withdraw(cls, Username: str, amount: float):
        Hall = cls.LoadTrnsactionsHall()
        if Username not in Hall['Username'].values:
            cls.TrnsactionsCompile = False, f'{cls.RootMessage} > Withdraw -> username not found'
            return

        current_balance = Hall.loc[Hall['Username'] == Username, 'Balance'].iloc[0]
        if current_balance < amount:
            cls.TrnsactionsCompile = False, f'{cls.RootMessage} > Withdraw -> insufficient funds'
            return

        Hall.loc[Hall['Username'] == Username, ['Balance', 'Date']] = \
            Hall.loc[Hall['Username'] == Username].assign(
                Balance=lambda df: df['Balance'] - amount,
                Date=cls.GetDateTime()
            )
        Hall.to_csv(cls.csvPath, index=False)
        cls.TrnsactionsCompile = True, f'{cls.RootMessage} > Withdraw -> withdrawal of {amount} successful'

    @classmethod
    def Transfer(cls, FromUsername: str, ToUsername: str, amount: float):
        Hall = cls.LoadTrnsactionsHall()
        if FromUsername not in Hall['Username'].values:
            cls.TrnsactionsCompile = False, f'{cls.RootMessage} > Transfer -> sender not found'
            return
        if ToUsername not in Hall['Username'].values:
            cls.TrnsactionsCompile = False, f'{cls.RootMessage} > Transfer -> receiver not found'
            return

        from_balance = Hall.loc[Hall['Username'] == FromUsername, 'Balance'].iloc[0]
        if from_balance < amount:
            cls.TrnsactionsCompile = False, f'{cls.RootMessage} > Transfer -> insufficient funds'
            return

        cls.Withdraw(FromUsername, amount)
        if not cls.TrnsactionsCompile[0] :
            return
        cls.Deposit(ToUsername, amount)
        if not cls.TrnsactionsCompile[0] :
            return

        cls.TrnsactionsCompile = True, f'{cls.RootMessage} > Transfer -> successfully transferred {amount} from {FromUsername} to {ToUsername}'

    @classmethod
    def GetBalance(cls, Username: str):
        Hall = cls.LoadTrnsactionsHall()
        if Username not in Hall['Username'].values:
            cls.TrnsactionsCompile = False, f'{cls.RootMessage} > GetBalance -> username not found'
            return

        balance = Hall.loc[Hall['Username'] == Username, 'Balance'].iloc[0]
        cls.TrnsactionsCompile = True, balance

    @classmethod
    def LoadTrnsactionsHall(cls):
        if not os.path.exists(cls.csvPath):
            os.makedirs(os.path.dirname(cls.csvPath), exist_ok=True)
            df = pd.DataFrame(columns=['Username', 'Password', 'Balance', 'Date'])
            df.to_csv(cls.csvPath, index=False)
            return df
        return pd.read_csv(cls.csvPath)

    @classmethod
    def GetDateTime(cls):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')