from ipv8.keyvault.crypto import default_eccrypto

with open("my_key.pem", "rb") as f:
    key_bin = f.read()

key = default_eccrypto.key_from_private_bin(key_bin)

print(key.pub().key_to_bin().hex())