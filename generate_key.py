from ipv8.keyvault.crypto import default_eccrypto

key = default_eccrypto.generate_key("curve25519")
with open("my_key.pem", "wb") as f:
    f.write(default_eccrypto.key_to_bin(key))

print("Public key (hex):", key.pub().key_to_bin().hex())
print("Key saved to my_key.pem")