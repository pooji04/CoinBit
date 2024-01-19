import keys
import time
import ecdsa
import json
import peer as p
import sql_connection as sql


def create_transaction(username, cursor, db, dest_ports, ip):
    while True:
        recipient = input("\nEnter recipient username: ")
        cursor.execute("select * from users where username = %s", (recipient, ))
        if not(cursor.fetchone()):
            print("That recipient does not exist.")
            continue

        amount = int(input("Enter amount: "))
        incentive = int(input("Enter incentive fee: "))

        cursor.execute("select amount from wallet where username = %s", (username,))
        available_amount = cursor.fetchone()
        available_amount = available_amount[0]

        if amount + incentive > int(available_amount):
            print("\nInsufficient balance. Please try again.")
            continue
        else:
            break

    available_amount = available_amount - amount - incentive

    cursor.execute("select bitcoin_address from users where username = %s", (username, ))
    sender_address = cursor.fetchone()
    sender_address = sender_address[0]

    cursor.execute("select bitcoin_address from users where username = %s", (recipient, ))
    recipient_address = cursor.fetchone()
    recipient_address = recipient_address[0]

    cursor.execute("select max(transaction_id) from transactions")
    ids = cursor.fetchone()
    ids = ids[0]
    if ids is None:
        ids = 0

    timestamp = time.time()
    
    transaction = {"Amount":int(amount),
                        "ID":int(ids + 1),
                        "Recipient Address":str(recipient_address),
                        "Sender Address":str(sender_address),
                        "Time":str(timestamp)}
    
    private_key = input("Please enter your private key for signing the transaction. It will not be stored anywhere: ")
    private_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key))
    signature = sign_transaction(private_key, transaction)
    signature = signature.decode('latin-1')

    cursor.execute("INSERT INTO transactions (Sender_Address, Recipient_Address, Amount, Time, Signature, Incentive) VALUES (%s, %s, %s, %s, %s, %s)",
               (sender_address, recipient_address, amount, timestamp, signature, incentive))
    db.commit()

    cursor.execute("update wallet set amount = %s where username = %s", (available_amount, username))
    cursor.execute("update wallet set amount = amount + %s where username = %s", (amount, recipient))
    p.send_messages("\nNew Transaction has been made.", ip, dest_ports)
    db.commit()

def sign_transaction(private_key, transaction_data):
    data_to_sign = json.dumps(transaction_data, sort_keys=True)
    signature = private_key.sign(data_to_sign.encode())
    return signature

def verify_transaction(public_key, signature, transaction_data):
    try:
        data_to_verify = json.dumps(transaction_data, sort_keys=True)
        return public_key.verify(signature, data_to_verify.encode())
    except ecdsa.BadSignatureError:
        return False

def verify_transactions(cursor, db, username):
    flag = True
    while flag:
        if not(return_information(cursor)):
            print("There are no transactions left to verify. Please try in some time.")
            break
        signature, transaction_data, public_key = return_information(cursor)
        if verify_transaction(public_key, signature, transaction_data):
            print("Transaction Verified.")
            cursor.execute("update transactions set verified = 'Verified' where Transaction_ID = %s", (transaction_data['ID'], ))
            db.commit()
            cursor.execute("select incentive from transactions where transaction_id = %s", (transaction_data['ID'], ))
            incentive = cursor.fetchone()
            incentive = incentive[0]
            cursor.execute("update wallet set amount = amount + %s where username = %s", (int(incentive), username))
            db.commit()
        else:
            print("This transaction is incorrect.")
            cursor.execute("update transactions set verified = 'Incorrect' where Transaction_Id = %s", (transaction_data['ID'], ))
            db.commit()
        flag = input("Do you want to continue verifying? (Yes/No): ")
        if flag == 'Yes':
            flag = True
        else:
            flag = False

def return_information(cursor):
    cursor.execute("SELECT * FROM transactions WHERE verified = 'Not Verified' order by incentive asc limit 1;")
    data = cursor.fetchone()
    if not(data):
        return
    signature = data[5]
    signature = signature.encode('latin-1')

    transaction_data = {"Amount":int(data[3]),
                        "ID":int(data[0]),
                        "Recipient Address":str(data[2]),
                        "Sender Address":str(data[1]),
                        "Time":str(data[4])}
    
    cursor.execute("select public_key from users where Bitcoin_Address = %s", (data[1], ))
    public_key = cursor.fetchone()
    public_key = public_key[0]
    public_key_bytes = bytes.fromhex(public_key)
    public_key_obj = ecdsa.VerifyingKey.from_string(public_key_bytes)

    return signature, transaction_data, public_key_obj

