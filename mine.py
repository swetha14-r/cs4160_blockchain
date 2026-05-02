import hashlib
import struct

email = "s.raghavendran@student.tudelft.nl"
github_url = "https://github.com/swetha14-r/cs4160_blockchain"

def check_28_leading_zero_bits(hash_bytes):
    return hash_bytes[0] == 0 and hash_bytes[1] == 0 and hash_bytes[2] == 0 and hash_bytes[3] < 16

prefix = email.encode("utf-8") + b"\n" + github_url.encode("utf-8") + b"\n"

print("Mining... this will take a few minutes")

nonce = 0
while True:
    nonce_bytes = struct.pack(">q", nonce)
    digest = hashlib.sha256(prefix + nonce_bytes).digest()
    if check_28_leading_zero_bits(digest):
        print(f"Found nonce: {nonce}")
        print(f"Hash: {digest.hex()}")
        break
    nonce += 1
    if nonce % 1_000_000 == 0:
        print(f"Tried {nonce} nonces...")