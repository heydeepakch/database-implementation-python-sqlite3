import sqlite3
import bcrypt

conn = sqlite3.connect('username_password.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY,
               name TEXT NOT NULL,
               username TEXT NOT NULL,
               salt TEXT NOT NULL,
               hash TEXT NOT NULL
    )
''')

def add_user():
    name = input("Enter your name: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    cursor.execute("INSERT INTO users (name, username, salt, hash) VALUES (?, ?, ?, ?)", (name, username, salt, hashed))
    conn.commit()
    print("User added successfully")

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    if user:
        hashed = bcrypt.hashpw(password.encode('utf-8'), user[3])
        if hashed == user[4]:
            print("Login successful")
            print("Thank You for using our app!")
            
        else:
            print("Invalid password")
    else:
        print("Invalid username")

def show_users():
    cursor.execute("SELECT name, username FROM users")
    users = cursor.fetchall()
    # print(users)
    for user in users:
        print(user)

def main():
    while True:
        print("\n Welcome to our App!\n")
        print("1. New User")
        print("2. Existing User")
        print("3. Show Users")
        print("4. Exit")
        
        choice = input("Enter your choice: ")

        match choice:
            case '1':
                add_user()
            case '2':
                login()
            case '3':
                show_users()
            case '4':
                break
            case _:
                print("Invalid Choice")

if __name__ == '__main__':
    main()