import time
import block as b
import sql_connection as sql

db = sql.create_sql_connection()
cursor = sql.create_sql_cursor(db)

global genesis_block
timestamp = time.time()
hash = b.calculate_hash(1, 0, timestamp, "Genesis Block")
genesis_block =  (1, 0, timestamp, "Genesis Block", hash)

cursor.execute("insert into blockchain(Previous_Block_Hash, Timestamp, Data, Hash_Value) values (%s, %s, %s, %s)", (0, timestamp, "Genesis Block", hash))
db.commit()