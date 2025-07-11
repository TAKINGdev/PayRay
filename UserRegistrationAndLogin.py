from datetime import datetime
import pandas as pd
import os

class TransactionsUserAccount:
    RegistrationedAccountsPath = 'UserAccounts/RegistrationedAccounts.csv'
    RootMessage = 'root > UserRegistrationAndLogin > TransactionsUserAccount'
    TransactionsRegistrationCompile = ''
    csvPath = 'TransactionsUserAccount/TransactionsUserAccountHall.csv'

    def __init__(self, Username: str, Password: str):
        if not self.isValidUsername(Username):
            self.TransactionsRegistrationCompile = f'{self.RootMessage} > init > not exist the valid username'
            return
        if not self.isMatchPassword(Username, Password):
            self.TransactionsRegistrationCompile = f'{self.RootMessage} > init > password does not match'
            return
        self.RegisterTransactionsAccount(Username, Password)
        self.TransactionsRegistrationCompile = f'{self.RootMessage} > init > registration the new transactions account was successfully'

    def isValidUsername(self, TargetUserName: str) -> bool:
        df = pd.read_csv(self.RegistrationedAccountsPath)
        return TargetUserName in df['Username'].values

    def isMatchPassword(self, Username: str, TargetPassword: str) -> bool:
        df = pd.read_csv(self.RegistrationedAccountsPath)
        user_row = df[df['Username'] == Username]
        if user_row.empty:
            return False
        real_password = user_row.iloc[0]['Password']
        return TargetPassword == real_password

    @classmethod
    def LoadAccount(cls):
        if not os.path.exists(cls.csvPath):
            os.makedirs(os.path.dirname(cls.csvPath), exist_ok=True)
            df = pd.DataFrame(columns=['Username', 'Password', 'Balance', 'Date'])
            df.to_csv(cls.csvPath, index=False)
            return df
        return pd.read_csv(cls.csvPath)

    @classmethod
    def RegisterTransactionsAccount(cls, Username: str, Password: str) :
        df = cls.LoadAccount()
        if Username in df['Username'].values:
            return
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        new_row = {'Username': Username, 'Password': Password, 'Balance': 0, 'Date' : timestamp}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(cls.csvPath, index=False)

    @classmethod
    def RegisterOutTransactionsAccount(cls, Username: str, Password: str) :
        df = cls.LoadAccount()
        Username = Username.strip()
        Password = Password.strip()

        condition = (df['Username'] == Username) & (df['Password'] == Password)
        if condition.any():
            df = df[~condition]
            df.to_csv(cls.csvPath, index=False)
            return True, f'{cls.RootMessage} > RegisterOutTransactionsAccount -> account successfully deleted'
        else:
            return False, f'{cls.RootMessage} > RegisterOutTransactionsAccount -> no matching account found'

class Registration:
    RootMessage = 'root > UserRegistrationAndLogin > registration'
    csvPath = 'UserAccounts/RegistrationedAccounts.csv'
    registrationCompile = ''
    
    def __init__(self, FirstName: str, LastName: str, Username: str, Password: str):
        FirstName = FirstName.strip().lower()
        LastName = LastName.strip().lower()
        Username = Username.strip().lower()

        if not self.isValidUsername(Username):
            self.registrationCompile = f'{self.RootMessage} > init -> target username is already registered'
            return
        
        if not self.isStrongPassword(Password):
            self.registrationCompile = f'{self.RootMessage} > init -> target password is WEAK'
            return
        
        self.RegisterAccount(FirstName, LastName, Username, Password)
        self.SyncWithTransaction(Username, Password)
        self.registrationCompile = f'{self.RootMessage} > init -> registration the new account was successfully'

    @classmethod
    def LoadAccount(cls):
        if not os.path.exists(cls.csvPath):
            os.makedirs(os.path.dirname(cls.csvPath), exist_ok=True)
            df = pd.DataFrame(columns=['FirstName', 'LastName', 'Username', 'Password'])
            df.to_csv(cls.csvPath, index=False)
            return df
        return pd.read_csv(cls.csvPath)

    
    @classmethod
    def RegisterAccount(cls, FirstName, LastName, Username, Password):
        df = cls.LoadAccount()
        new_row = {
            'FirstName': FirstName.lower().strip(),
            'LastName': LastName.lower().strip(),
            'Username': Username,
            'Password': Password
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(cls.csvPath, index=False)

    @classmethod
    def isValidUsername(cls, TargetUserName: str) -> bool:
        df = cls.LoadAccount()
        df['Username'] = df['Username'].astype(str).str.strip().str.lower()
        TargetUserName = TargetUserName.strip().lower()
        return TargetUserName not in df['Username'].values

    @staticmethod
    def isStrongPassword(password: str) -> bool:
        if len(password) < 8:
            return False

        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)

        return has_upper and has_lower and has_digit
    
    def SyncWithTransaction(self, Username, Password):
        TransactionsUserAccount.RegisterTransactionsAccount(Username, Password)
    
class RegistrationOut:
    RootMessage = 'root > UserRegistrationAndLogin > registration out'
    csvPath = 'UserAccounts/RegistrationedAccounts.csv'
    registrationCompile = ''

    def __init__(self, FirstName, LastName, Username, Password):
        FirstName = FirstName.strip().lower()
        LastName = LastName.strip().lower()
        Username = Username.strip().lower()

        self.registrationCompile = self.isRegistered(FirstName, LastName, Username)
        if not self.registrationCompile[0]:
            self.registrationCompile = self.registrationCompile[1]
            return
        
        self.registrationCompile = self.isMathPassword(Username, Password)
        if not self.registrationCompile[0]:
            self.registrationCompile = self.registrationCompile[1]
            return
        self.RemoveFromTransaction(Username, Password)
        self.registrationCompile = self.DropRegistrationedAccount(FirstName, LastName, Username)

    @staticmethod
    def isRegistered(FirstName: str, LastName: str, Username: str):
        df = pd.read_csv(RegistrationOut.csvPath)
        df['FirstName'] = df['FirstName'].astype(str).str.strip().str.lower()
        df['LastName'] = df['LastName'].astype(str).str.strip().str.lower()
        df['Username'] = df['Username'].astype(str).str.strip().str.lower()

        if FirstName not in df['FirstName'].values:
            return False, f'{Registration.RootMessage} > init > isRegistered -> first name not found'
        if LastName not in df['LastName'].values:
            return False, f'{Registration.RootMessage} > init > isRegistered -> last name not found'
        if Username not in df['Username'].values:
            return False, f'{Registration.RootMessage} > init > isRegistered -> username not found'

        condition = (
            (df['FirstName'] == FirstName) &
            (df['LastName'] == LastName) &
            (df['Username'] == Username)
        )

        if condition.any():
            return True, ''
        else:
            return False, f'{Registration.RootMessage} > init > isRegistered -> no exact match for full identity'
    
    @staticmethod
    def isMathPassword(Username: str, TargetPassword: str):
        df = pd.read_csv(RegistrationOut.csvPath)
        df['Username'] = df['Username'].astype(str).str.strip().str.lower()
        Username = Username.strip().lower()
        TargetPassword = TargetPassword.strip()

        user_row = df[df['Username'] == Username]
        if user_row.empty:
            return False, f'{Registration.RootMessage} > init > isMathPassword -> username not found'

        real_password = user_row.iloc[0]['Password']
        if TargetPassword == real_password:
            return True, ''
        else:
            return False, f'{Registration.RootMessage} > init > isMathPassword -> password does not match'

    def DropRegistrationedAccount(self, FirstName, LastName, Username):
        df = pd.read_csv(self.csvPath)
        df['FirstName'] = df['FirstName'].astype(str).str.strip().str.lower()
        df['LastName'] = df['LastName'].astype(str).str.strip().str.lower()
        df['Username'] = df['Username'].astype(str).str.strip().str.lower()

        condition = (
            (df['FirstName'] == FirstName) &
            (df['LastName'] == LastName) &
            (df['Username'] == Username)
        )

        df = df[~condition]
        df.to_csv(self.csvPath, index=False)
        return f'{self.RootMessage} > init > DropRegistrationedAccount -> account successfully deleted'

    def RemoveFromTransaction(self, Username, Password) :
        TransactionsUserAccount.RegisterOutTransactionsAccount(Username, Password)