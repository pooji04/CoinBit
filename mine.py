import hashlib
import random
import time
import peer

def sha256_hash(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def generate_difficulty_target():
    target_bits = 256
    target_hex = ''.join(random.choice('0123456789abcdef') for _ in range(target_bits // 4))
    return target_hex

message_received = False

def mine_block(db, cursor, dest_ports, username, ip):
    flag = True

    while flag:
        cursor.execute("""SELECT Transaction_ID, Sender_Address, Recipient_Address, Amount, Time, Signature
                    FROM transactions
                    WHERE added = 'Not Added' AND verified = 'Verified'
                    ORDER BY incentive ASC
                    LIMIT 5;
                    """)
        data = cursor.fetchall()
        if data == []:
            print("There are no verified transactions. Please try after some time.")
            return
        keys_list = ['ID', 'Sender Address', 'Recipient Address', 'Amount', 'Time', 'Signature']

        transaction_data = [{key: value for key, value in zip(keys_list, values)} for values in data]
        ids = tuple(value[0] for value in data)

        cursor.execute("SELECT Hash_Value FROM blockchain WHERE Block_ID = (SELECT MAX(Block_ID) FROM blockchain)")
        prev_hash_value = cursor.fetchone()
        prev_hash_value = prev_hash_value[0] 
        block_header = prev_hash_value + ''.join(str(transaction) for transaction in transaction_data)
        difficulty_target = generate_difficulty_target()
        nonce = 0

        flag1 = True
        while flag1:
            candidate_block = block_header + format(nonce, 'x')
            block_hash = sha256_hash(candidate_block)

            if block_hash < difficulty_target:  
                peer.send_messages("Mining completed by peer.", ip, dest_ports)
                cursor.execute("insert into blockchain (Previous_Block_Hash, Timestamp, Data, Hash_Value) values (%s, %s, %s, %s)", (prev_hash_value, time.time(), str(transaction_data), block_hash))
                db.commit()

                print("Bitcoin reward added.")
                cursor.execute("update wallet set amount = amount + 20 where username = %s", (username, ))
                db.commit()

                placeholders = ', '.join(['%s'] * len(ids))
                query = f"UPDATE transactions SET added = 'Added' WHERE transaction_id IN ({placeholders})"
                cursor.execute(query, tuple(ids))
                db.commit()
                flag1 = False
            else:
                nonce += 1

        answer = input("Do you want to continue mining? (Yes/No):")
        if answer == 'Yes':
            flag = True
        else:
            flag = False