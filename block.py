import hashlib
import time
import json
import pprint

def calculate_hash(index, previous_hash, timestamp, data):
    block_string = f"{index}{previous_hash}{timestamp}{json.dumps(data)}"
    return hashlib.sha256(block_string.encode()).hexdigest()

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = int(time.time())
    hash = calculate_hash(index, previous_block.hash, timestamp, data)
    return tuple(index, previous_block.hash, timestamp, data, hash)

def display_blockchain(cursor, db):
    cursor.execute("select * from blockchain")
    data = cursor.fetchall()
    pprint.pprint(data)
