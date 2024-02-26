import tkinter as tk

class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        #self.open_trades = open_trades

class AccountVisualizer:
    def __init__(self, accounts):
        self.accounts = accounts
        
        self.root = tk.Tk()
        self.root.title("Account Visualizer")
        
        self.create_widgets()
        self.update_ui()
        
    def create_widgets(self):
        self.account_frame = tk.Frame(self.root)
        self.account_frame.pack(padx=10, pady=10)
        
        self.labels = []
        for account in self.accounts:
            account_label = tk.Label(self.account_frame)
            account_label.pack(anchor="w", padx=5, pady=2)
            self.labels.append(account_label)
        
    def update_ui(self):
        for i, account in enumerate(self.accounts):
            self.labels[i].config(text=f"Name: {account.name}, Balance: {account.balance}")
        
        # Schedule the next update after 1 second
        self.root.after(1000, self.update_ui)
        
    def run(self):
        self.root.mainloop()

## Sample account data
#accounts = [
#    Account("Account 1", 1000, 3),
#    Account("Account 2", 2000, 2),
#    Account("Account 3", 1500, 1)
#]
#
## Create and run the account visualizer
#visualizer = AccountVisualizer(accounts)
#visualizer.run()
