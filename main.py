import user as u
import transactions as t
import sql_connection as sql
import wallet as w
import block as b
import mine as m
import threading
import peer
import socket
import time

db = sql.create_sql_connection()
cursor = sql.create_sql_cursor(db)

while True:
    print("Welcome to CoinBit.")
    print("1. Login")
    print("2. Signup")
    print("3. Exit")
    choice = input("Select an option: ")
    print()

    if choice == '1':
        flag = True
        while flag:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            flag = u.login(cursor, username, password)
        break

    elif choice == '2':
        u.signup(cursor, db)
        print("You will be redirected to main page. Please login with your new credentials.\n")

    elif choice == '3':
        print("Thank you for using CoinBit.")
        time.sleep(3)
        exit()

    else:
        print("The choice is not available. Please try again.\n")

cursor.execute("select port_number from users_port where username = %s", (username, ))
port = cursor.fetchone()
port = port[0]
ip = socket.gethostbyname(socket.gethostname())
cursor.execute("SELECT port_number FROM users_port")
result_set = cursor.fetchall()
dest_ports = [row[0] for row in result_set]
peer_process = threading.Thread(target = peer.start_peer,args = (port, ip, cursor),daemon = True)
peer_process.start()

while True:
    print("\n Main Menu Options.")
    print("1. Mine")
    print("2. Verify Transaction")
    print("3. Create Transaction")
    print("4. Display Wallet")
    print("5. Display Blockchain")
    print("6. Exit")
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        m.mine_block(db, cursor, dest_ports, username, ip)

    elif choice == 2:
        t.verify_transactions(cursor, db, username)

    elif choice == 3:
        t.create_transaction(username, cursor, db, dest_ports, ip)

    elif choice == 4:
        w.display_wallet(username, cursor, db)

    elif choice == 5:
        b.display_blockchain(cursor, db)

    elif choice == 6:
        print("\nThank you for using CoinBit.")
        break

    else:
        print("That is the wrong option. Please try again.\n")