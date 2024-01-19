# CoinBit - A Simplified Bitcoin Model with Peer-to-Peer Architecture

The CoinBit project aims to replicate the Bitcoin model with a peer-to-peer architecture. The implementation involves several steps and modules. Follow the steps below to set up and run the project.

## 1. Creating a Database

### a) Users Table
- Details regarding the user/miner, cryptographic keys, and bitcoin addresses.
  
### b) Transactions Table
- Records details about transactions, including sender and recipient addresses, transaction amount, timestamp, digital signatures, transaction incentives, and verification status.

### c) Blockchain Table
- Stores information about blocks, including block identification, the hash of the previous block, timestamp, block data, and the current block’s hash value.

### d) Wallet Table
- Records the amount of cryptocurrency associated with each user.

### e) User_port Table
- Helps in network communication by storing port numbers for each user.

## 2. Creating a Block Module

This module contains key functions to implement the blockchain module, such as `calculate_hash`, `create_new_block`, and `display_blockchain`.

## 3. Creating an SQL Connection Module

Functions to connect and edit the database, including `create_sql_connection`, `create_sql_cursor`, and `close_connection`.

## 4. Initializing the Database Connection and Adding Blocks to a Chain

Create an SQL connection using the `sql_connection` module, initialize a connection and cursor, and add blocks to the blockchain.

## 5. Module to Generate Keys

Functions to generate key pairs and corresponding Bitcoin addresses using the `ecdsa` library.

## 6. Creating a Signup System/User Module

Functions to create new users, verify details, and login. Passwords are encrypted using SHA-256, and emails are verified using regular expressions.

## 7. Creating a Peer Module

Establishes a simple peer-to-peer communication system using sockets in Python. Functions to assign port numbers, start a peer server, and send messages to peers.

## 8. Defining Transactions Module

Implements transaction-related functionalities, including creating, signing, and verifying transactions. Uses the `ecdsa` library for elliptic curve cryptography and interacts with the database.

## 9. Defining the Mine Module

The main functionality for mining involves miners competing to find a nonce that satisfies the difficulty target. Once successful, a new block is added to the blockchain, and the associated transactions are marked as added.

## 10. The Main Function

Acts as the user interface, allowing users to log in or sign up. Displays a main menu with options to mine, verify/create transactions, display the wallet, display the blockchain, or exit the application.

## Steps to Run CoinBit

1. Create a database called `coinbit` in MySQL.
2. Run the `tables.py` file to initialize the tables.
3. Run the `start.py` file to create the genesis block.
4. Run the `main.py` file to interact with the CoinBit system.

## Required Modules

Install the following Python modules:
```bash
pip install mysql.connector hashlib time json pprint ecdsa base58 smtplib socket threading re random
```

Note: The project currently has a limitation where only one peer can mine at a time. Future iterations could focus on optimizing the mining process for concurrent mining by multiple peers to enhance scalability and decentralization.
