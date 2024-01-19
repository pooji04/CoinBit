import ecdsa
import hashlib
import base58

def generate_key_pair():
    private_key = ecdsa.SigningKey.generate()
    public_key = private_key.get_verifying_key()
    private_key_string = private_key.to_string().hex()
    public_key_string = public_key.to_string().hex()
    return private_key_string, public_key_string

def generate_bitcoin_address(public_key_string):
    sha256_hash = hashlib.sha256(bytes.fromhex(public_key_string)).digest()

    ripemd160_hash = hashlib.new('ripemd160')
    ripemd160_hash.update(sha256_hash)
    ripemd160_hash_result = ripemd160_hash.digest()

    extended_hash = b'\x00' + ripemd160_hash_result

    sha256_hash = hashlib.sha256(extended_hash).digest()
    sha256_hash = hashlib.sha256(sha256_hash).digest()

    checksum = sha256_hash[:4]
    binary_address = extended_hash + checksum

    bitcoin_address = base58.b58encode(binary_address).decode('utf-8')

    return bitcoin_address


