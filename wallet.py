def display_wallet(username, cursor, db):
    cursor.execute("select amount from wallet where username = %s", (username,))
    balance = cursor.fetchone()
    balance = balance[0]
    print("\nCurrent Wallet Balance (in CoinBits): ", balance)