import sql_connection as sql

db = sql.create_sql_connection()
cursor = sql.create_sql_cursor(db)

cursor.execute("""create table if not exists users
               (User_ID INT AUTO_INCREMENT PRIMARY KEY,
               Name VARCHAR(200), 
               Email_ID VARCHAR(200), 
               Username VARCHAR(200), 
               Password VARCHAR(256),
               Public_Key VARCHAR(500),
               Bitcoin_Address VARCHAR(300))""")
db.commit()

cursor.execute("""create table if not exists transactions
               (Transaction_ID INT AUTO_INCREMENT PRIMARY KEY,
               Sender_Address VARCHAR(200), 
               Recipient_Address VARCHAR(200), 
               Amount VARCHAR(200), 
               Time VARCHAR(300),
               Signature VARCHAR(300),
               Incentive int(10),
               Verified VARCHAR(20) DEFAULT 'Not Verified',
               Added VARCHAR(10) DEFAULT 'Not Added')""")
db.commit()

cursor.execute("""create table if not exists Blockchain
               (Block_ID INT AUTO_INCREMENT PRIMARY KEY,
               Previous_Block_Hash VARCHAR(300),
               Timestamp VARCHAR(200), 
               Data varchar(2000), 
               Hash_Value VARCHAR(300))""")
db.commit()

cursor.execute("""create table if not exists wallet
               (Username varchar(200), 
               Amount int(20))""")
db.commit()

cursor.execute("""create table if not exists users_port
               (Username VARCHAR(200),
               Port_Number int(10))""")
db.commit()