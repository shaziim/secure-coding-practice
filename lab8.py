import sqlite3
import os
import hashlib

# Vulnerable: Database connection without proper handling
def connect_to_db():
    conn = sqlite3.connect("users.db")
    return conn.cursor()

# Vulnerable: No input sanitization for username or password
def register_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    # Vulnerable: Plaintext password storage
    hashed_password = hashlib.md5(password.encode()).hexdigest()  # Weak hashing method

    cursor = connect_to_db()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    print("User registered successfully!")

# Vulnerable: SQL Injection vulnerability (no input validation)
def login_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    # Vulnerable: Weak password verification logic
    hashed_password = hashlib.md5(password.encode()).hexdigest()  # Weak hashing method
    
    cursor = connect_to_db()
    # Vulnerable: Direct user input in SQL query (SQL injection)
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed_password}'")
    user = cursor.fetchone()
    
    if user:
        print("Login successful!")
    else:
        print("Invalid username or password.")

# Vulnerable: No input validation or sanitization in this function
def delete_user():
    username = input("Enter username to delete: ")
    
    cursor = connect_to_db()
    # Vulnerable: SQL injection possibility
    cursor.execute(f"DELETE FROM users WHERE username = '{username}'")
    print(f"User {username} deleted successfully!")

# Vulnerable: Arbitrary file reading with no validation
def view_file():
    filename = input("Enter filename to view: ")
    
    # Vulnerable: Path traversal vulnerability
    with open(filename, "r") as file:
        print(file.read())

# Vulnerable: System command execution with no validation
def execute_command():
    command = input("Enter shell command: ")
    
    # Vulnerable: Arbitrary shell command execution
    os.system(command)

# Main menu for the application
def main():
    while True:
        print("\nOptions:")
        print("1) Register User")
        print("2) Login User")
        print("3) Delete User")
        print("4) View File")
        print("5) Execute Command")
        print("6) Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            delete_user()
        elif choice == "4":
            view_file()
        elif choice == "5":
            execute_command()
        elif choice == "6":
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
