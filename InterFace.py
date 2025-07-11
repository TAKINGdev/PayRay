import customtkinter as ctk
from tkinter import messagebox
from UserRegistrationAndLogin import Registration, RegistrationOut, TransactionsUserAccount
from FinancialTransactions import Transactions as Trnsactions

class RegistrationUI:
    def __init__(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()
        self.app.title("User Registration and Removal")
        self.app.geometry("500x600")

        self.mode = ctk.StringVar(value="Sign In")

        ctk.CTkLabel(self.app, text="Choose Mode:", font=("Arial", 16)).pack(pady=10)
        ctk.CTkSegmentedButton(self.app, values=["Sign In", "Sign Out"], variable=self.mode,
                               command=self.update_form).pack()

        self.first_name_entry = ctk.CTkEntry(self.app, placeholder_text="First Name")
        self.last_name_entry = ctk.CTkEntry(self.app, placeholder_text="Last Name")
        self.username_entry = ctk.CTkEntry(self.app, placeholder_text="Username")
        self.password_entry = ctk.CTkEntry(self.app, placeholder_text="Password", show="*")

        self.first_name_entry.pack(pady=10)
        self.last_name_entry.pack(pady=10)
        self.username_entry.pack(pady=10)
        self.password_entry.pack(pady=10)

        self.action_button = ctk.CTkButton(self.app, text="Submit", command=self.handle_action)
        self.action_button.pack(pady=20)

        self.result_label = ctk.CTkLabel(self.app, text="")
        self.result_label.pack(pady=20)

        self.app.mainloop()

    def update_form(self, _=None):
        mode = self.mode.get()
        if mode == "Sign In":
            self.password_entry.configure(placeholder_text="Password", show="*")
            self.action_button.configure(text="Register")
        elif mode == "Sign Out":
            self.password_entry.configure(placeholder_text="Password", show="*")
            self.action_button.configure(text="Delete Account")

    def handle_action(self):
        fname = self.first_name_entry.get().strip()
        lname = self.last_name_entry.get().strip()
        uname = self.username_entry.get().strip()
        pwd = self.password_entry.get().strip()

        if not fname or not lname or not uname or not pwd:
            self.result_label.configure(text="Please fill all fields", text_color="red")
            return

        if self.mode.get() == "Sign In":
            result = Registration(fname, lname, uname, pwd)
            msg = result.registrationCompile
        else:
            result = RegistrationOut(fname, lname, uname, pwd)
            msg = result.registrationCompile

        self.result_label.configure(text=msg, text_color="green" if "successfully" in msg else "red")

class UserDashboard(ctk.CTkToplevel):
    def __init__(self, Username):
        super().__init__()
        self.title("User Dashboard")
        self.geometry("400x400")
        self.Username = Username

        ctk.CTkLabel(self, text=f"Welcome, {Username}", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        ctk.CTkButton(self, text="Check Balance", command=self.check_balance).pack(pady=5)

        self.deposit_entry = ctk.CTkEntry(self, placeholder_text="Deposit Amount")
        self.deposit_entry.pack(pady=5)
        ctk.CTkButton(self, text="Deposit", command=self.deposit).pack(pady=5)

        self.withdraw_entry = ctk.CTkEntry(self, placeholder_text="Withdraw Amount")
        self.withdraw_entry.pack(pady=5)
        ctk.CTkButton(self, text="Withdraw", command=self.withdraw).pack(pady=5)

        self.transfer_to_entry = ctk.CTkEntry(self, placeholder_text="Transfer to (username)")
        self.transfer_to_entry.pack(pady=5)
        self.transfer_amount_entry = ctk.CTkEntry(self, placeholder_text="Amount to Transfer")
        self.transfer_amount_entry.pack(pady=5)
        ctk.CTkButton(self, text="Transfer", command=self.transfer).pack(pady=5)

        ctk.CTkButton(self, text="Logout", command=self.destroy).pack(pady=10)

    def check_balance(self):
        Trnsactions.GetBalance(self.Username)
        success, result = Trnsactions.TrnsactionsCompile
        if success:
            messagebox.showinfo("Balance", f"Your balance is: {result}")
        else:
            messagebox.showerror("Error", result)

    def deposit(self):
        try:
            amount = float(self.deposit_entry.get())
            Trnsactions.Deposit(self.Username, amount)
            success, msg = Trnsactions.TrnsactionsCompile
            messagebox.showinfo("Deposit", msg if success else "Error: " + msg)
        except:
            messagebox.showerror("Error", "Invalid deposit amount")

    def withdraw(self):
        try:
            amount = float(self.withdraw_entry.get())
            Trnsactions.Withdraw(self.Username, amount)
            success, msg = Trnsactions.TrnsactionsCompile
            messagebox.showinfo("Withdraw", msg if success else "Error: " + msg)
        except:
            messagebox.showerror("Error", "Invalid withdrawal amount")

    def transfer(self):
        to_user = self.transfer_to_entry.get().strip()
        try:
            amount = float(self.transfer_amount_entry.get())
            Trnsactions.Transfer(self.Username, to_user, amount)
            success, msg = Trnsactions.TrnsactionsCompile
            messagebox.showinfo("Transfer", msg if success else "Error: " + msg)
        except:
            messagebox.showerror("Error", "Invalid transfer data")

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login to Account")
        self.geometry("350x300")

        ctk.CTkLabel(self, text="User Login", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        ctk.CTkButton(self, text="Login", command=self.try_login).pack(pady=15)

        ctk.CTkButton(self, text="Exit", fg_color="red", hover_color="#cc0000", command=self.quit).pack(pady=5)

    def try_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        login_user = TransactionsUserAccount(username, password)
        result = login_user.TransactionsRegistrationCompile

        if "successfully" in result:
            messagebox.showinfo("Success", "Login successful!")
            dashboard = UserDashboard(username)
            dashboard.grab_set()
        else:
            messagebox.showerror("Login Failed", result)

if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    app = LoginApp()
    app.mainloop()