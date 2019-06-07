# --------
# Generating a private key from a random number
# --------
# source: Chapter 4 Bitcoin Book Andreas Antonopoulos

# Pick a number between 0 and n - 1, any method that is certainly unpredictable
# where n = 2^256 - 2^32 - 2^9 - 2^8 - 2^7 - 2^6 - 2^4 - 1
# (slightly less than 2^256)

# Bitcoin software uses the computer's operating system
# to generate a random number, usually generator is initialized
# with human source or randomness, like wiggling your mouse

# private key can be any number between 0 and n - 1 inclusive
# Method:
# Find a cryptographically secure source of entropy randomness
# Randomly pick 256-bit number repeatly until it's less than n
# Randomly picking:
# feed a larger string or random bits from the secure source
# into sha256 algorithm with conviniently produces a 256 number


import hashlib
import secrets

n = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1
private_key = 0 # will be bytes

while True:

    h = hashlib.sha256()
    h.update(secrets.token_bytes(32)) # 32 bytes / 256 bits
    private_key = h.digest()
    m = int.from_bytes(private_key, byteorder="big")

    if m < n :
        break

print("\n-----")
print("PRIVATE KEY")
print("-----")

print("\nIn bytes:\n", private_key)
print("\nIn hex:\n", private_key.hex())

print("\n-----")
