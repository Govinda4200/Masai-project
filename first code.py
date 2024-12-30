import hashlib
import datetime

# Function to create a new account
def create_account(accounts):
    # Get user details
    name = input("Enter your name: ")
    initial_deposit = float(input("Enter your initial deposit: "))
    account_number = str(len(accounts) + 1).zfill(6)  # Generate account number
    password = hashlib.sha256(input("Enter a password: ").encode()).hexdigest()  # Hash the password
    accounts[account_number] = [name, password, initial_deposit]
    
    # Write account details to file
    with open('accounts.txt', 'a') as f:
        f.write(f"{account_number},{name},{password},{initial_deposit}\n")
    print(f"Your account number: {account_number}\nAccount created successfully!")

# Function to login
def login(accounts):
    account_number = input("Enter your account number: ")
    password = hashlib.sha256(input("Enter your password: ").encode()).hexdigest()
    if account_number in accounts and accounts[account_number][1] == password:
        print("Login successful!")
        return account_number
    else:
        print("Invalid account number or password!")
        return None

# Function to deposit money
def deposit(account_number, accounts):
    amount = float(input("Enter amount to deposit: "))
    accounts[account_number][2] += amount  # Update balance
    
    # Update accounts file
    with open('accounts.txt', 'w') as f:
        for acc, details in accounts.items():
            f.write(f"{acc},{details[0]},{details[1]},{details[2]}\n")
    
    # Log the transaction
    with open('transactions.txt', 'a') as f:
        f.write(f"{account_number},Deposit,{amount},{datetime.date.today()}\n")
    print(f"Deposit successful! Current balance: {accounts[account_number][2]}")

# Function to withdraw money
def withdraw(account_number, accounts):
    amount = float(input("Enter amount to withdraw: "))
    if amount <= accounts[account_number][2]:
        accounts[account_number][2] -= amount  # Update balance
        
        # Update accounts file
        with open('accounts.txt', 'w') as f:
            for acc, details in accounts.items():
                f.write(f"{acc},{details[0]},{details[1]},{details[2]}\n")
        
        # Log the transaction
        with open('transactions.txt', 'a') as f:
            f.write(f"{account_number},Withdrawal,{amount},{datetime.date.today()}\n")
        print(f"Withdrawal successful! Current balance: {accounts[account_number][2]}")
    else:
        print("Insufficient balance!")

# Main function
def main():
    accounts = {}
    try:
        # Load accounts from file
        with open('accounts.txt', 'r') as f:
            for line in f:
                account_number, name, password, balance = line.strip().split(',')
                accounts[account_number] = [name, password, float(balance)]
    except FileNotFoundError:
        pass

    # Main menu loop
    while True:
        print("\nWelcome to the Banking System!")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            create_account(accounts)
        elif choice == '2':
            account_number = login(accounts)
            if account_number:
                # Logged in menu loop
                while True:
                    print("\n1. Deposit")
                    print("2. Withdraw")
                    print("3. Logout")
                    user_choice = input("Enter your choice: ")
                    if user_choice == '1':
                        deposit(account_number, accounts)
                    elif user_choice == '2':
                        withdraw(account_number, accounts)
                    elif user_choice == '3':
                        break
                    else:
                        print("Invalid choice!")
        elif choice == '3':
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
