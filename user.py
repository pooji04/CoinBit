import hashlib
import re
import keys
import mail as m
import peer as p

class User:
    
    def __init__(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()


def login(cursor, username, password):
    while True:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
        if cursor.fetchone():
            print("\nUser Verified.")
            return False
        else:
            print("\nWrong Username or Password. Please try again.")
            return True

def signup(cursor, db):
    print("Welcome to the signup page. Please enter the following information.")
    name = input("\nEnter your name: ")
    print("Please ensure you are entering a verified email address as your key will be sent to this address.")
    email = input("Enter your email address: ")
    while not is_valid_email(email):
        print("\nThe email address is invalid. Please try again.")
        email = input("Enter your email address: ")

    while True:
        username = input("Enter your username: ")
        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            print("\nThis username has already been taken. Please try another username.")
        else:
            break
    
    password = input("Enter password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    private_key, public_key = keys.generate_key_pair()
    bitcoin_address = keys.generate_bitcoin_address(public_key)

    m.send_mail(email, private_key)                              
    
    cursor.execute("INSERT INTO users (name, email_id, username, password, public_key, bitcoin_address) VALUES (%s, %s, %s, %s, %s, %s)",
                   (name, email, username, hashed_password, public_key, bitcoin_address))
    db.commit()

    cursor.execute("INSERT INTO wallet (Username, Amount) VALUES (%s, %s)", (username, 0))
    db.commit()

    port_number = p.assignPort(username, cursor, db)
    cursor.execute("INSERT INTO users_port (Username, Port_Number) VALUES (%s, %s)", (username, port_number))
    db.commit()

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    match = re.match(pattern, email)
    return bool(match)