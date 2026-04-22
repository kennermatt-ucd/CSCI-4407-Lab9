import random

# Diffie-Hellman Key Exchange

# Publicly agreed-upon values
p = 23   # prime modulus
g = 5    # primitive root (generator)

# --- Alice ---
a = random.randint(2, p - 2)        # Alice's private key
A = pow(g, a, p)                    # Alice's public key: A = g^a mod p

# --- Bob ---
b = random.randint(2, p - 2)        # Bob's private key
B = pow(g, b, p)                    # Bob's public key: B = g^b mod p

# --- Key Exchange ---
alice_shared = pow(B, a, p)         # Alice computes: B^a mod p
bob_shared   = pow(A, b, p)         # Bob computes:   A^b mod p

# --- Output ---
print(f"Public values:     p={p}, g={g}")
print(f"Alice private key: a={a}")
print(f"Bob   private key: b={b}")
print(f"Alice public key:  A = g^a mod p = {A}")
print(f"Bob   public key:  B = g^b mod p = {B}")
print(f"Alice shared key:  B^a mod p = {alice_shared}")
print(f"Bob   shared key:  A^b mod p = {bob_shared}")
print(f"Keys match: {alice_shared == bob_shared}")
