Yes — we can **rebuild the entire lab in a clean, usable format** so you don’t lose anything from the PDF. I’ll condense it into a **clear, structured, copy-paste-ready version** with ALL required steps + code preserved.

---

# 🔐 **CSCI 4407 – Lab 9 Rebuilt (Clean Version)**

**Key Distribution, PKI, Diffie-Hellman, MITM**

---

# 🧩 **Lab Goal (Plain English)**

You are proving:

1. Encryption alone is **NOT secure**
2. Trust (authentication) is required
3. PKI fixes trust issues
4. Diffie-Hellman works… but fails under MITM
5. Real systems (TLS) combine everything

---

# ⚙️ **Setup**

```bash
sudo apt update
sudo apt install openssl python3 python3-pip
```

```bash
mkdir Key_Distribution_Lab
cd Key_Distribution_Lab
```

---

# 🧪 **TASK 1 – Setup + Files**

```bash
echo "Confidential payroll report for Alice." > msg1.txt
echo "Server backup credentials for secure transfer." > msg2.txt
echo "Session initialization data for Bob." > msg3.txt

cat msg1.txt
cat msg2.txt
cat msg3.txt

pwd
ls -l

sha256sum msg1.txt msg2.txt msg3.txt
```

### ✏️ Explain

* Why real files help visualize attacks
* Why data matters if attacker gets it

---

# 🧠 **TASK 2 – Public Key Attack (HANDWRITTEN)**

### Intended:

```
Alice → pkA → Bob  
Bob encrypts with pkA  
Alice decrypts with skA
```

### Attack:

```
Eve replaces pkA with pkE  
Bob encrypts with pkE  
Eve decrypts with skE
```

### ✏️ Explain

* Bob thinks he is secure
* Eve reads everything
* No one detects attack

---

# 🔑 **TASK 3 – Generate Alice Keys**

```bash
openssl genpkey -algorithm RSA -out alice_private.pem -pkeyopt rsa_keygen_bits:2048

openssl rsa -pubout -in alice_private.pem -out alice_public.pem

ls -l alice_private.pem alice_public.pem
```

(Optional)

```bash
openssl pkey -in alice_private.pem -text -noout
openssl rsa -pubin -in alice_public.pem -text -noout
```

### ✏️ Explain

* Private key = secret
* Public key = shareable
* BUT still not trusted

---

# 🏛️ **TASK 4 – Create CA**

```bash
openssl genpkey -algorithm RSA -out ca_private.pem -pkeyopt rsa_keygen_bits:2048

openssl req -x509 -new -key ca_private.pem -out ca_cert.pem -days 3650
```

```bash
openssl x509 -in ca_cert.pem -text -noout
ls -l ca_private.pem ca_cert.pem
```

### ✏️ Explain

* CA = trusted authority
* Root of trust

---

# 📄 **TASK 5 – Create CSR**

```bash
openssl req -new -key alice_private.pem -out alice.csr
```

```bash
openssl req -in alice.csr -text -noout
ls -l alice.csr
```

### ✏️ Explain

* CSR = request to verify identity
* Contains public key + identity

---

# 🏷️ **TASK 6 – Issue Certificate**

```bash
openssl x509 -req -in alice.csr -CA ca_cert.pem -CAkey ca_private.pem \
-CAcreateserial -out alice_cert.pem -days 365 -sha256
```

```bash
openssl x509 -in alice_cert.pem -text -noout
ls -l alice_cert.pem ca_cert.srl
```

### ✏️ Explain

* CA signs Alice’s identity + key
* Now key is **trusted**

---

# ✅ **TASK 7 – Verify Certificate**

```bash
openssl verify -CAfile ca_cert.pem alice_cert.pem
```

```bash
openssl x509 -in alice_cert.pem -noout -subject -issuer
openssl x509 -in alice_cert.pem -noout -dates
```

### ✏️ Explain

* Valid ONLY if CA is trusted
* Trust = anchored in CA

---

# 🚨 **TASK 8 – Fake CA (IMPORTANT)**

```bash
openssl genpkey -algorithm RSA -out fake_ca_private.pem -pkeyopt rsa_keygen_bits:2048

openssl req -x509 -new -key fake_ca_private.pem -out fake_ca_cert.pem -days 3650
```

```bash
openssl genpkey -algorithm RSA -out eve_private.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in eve_private.pem -out eve_public.pem
```

```bash
openssl req -new -key eve_private.pem -out eve.csr
```

```bash
openssl x509 -req -in eve.csr -CA fake_ca_cert.pem -CAkey fake_ca_private.pem \
-CAcreateserial -out eve_cert.pem -days 365 -sha256
```

```bash
# Works
openssl verify -CAfile fake_ca_cert.pem eve_cert.pem

# Fails
openssl verify -CAfile ca_cert.pem eve_cert.pem
```

### ✏️ Explain

* Trust depends on **which CA you accept**
* This is how attacks happen in real life

---

# 🔢 **TASK 9 – Diffie-Hellman (Python)**

```python
p = 23
g = 5

x = 6
y = 15

X = pow(g, x, p)
Y = pow(g, y, p)

KA = pow(Y, x, p)
KB = pow(X, y, p)

print("Public prime p =", p)
print("Generator g =", g)
print("Alice secret x =", x)
print("Bob secret y =", y)
print("Alice sends X =", X)
print("Bob sends Y =", Y)
print("Alice computes KA =", KA)
print("Bob computes KB =", KB)
print("Same key?", KA == KB)
```

```bash
python3 dh_demo.py
```

### ✏️ Explain

* Both compute same key
* Without sharing secrets

---

# 👀 **TASK 10 – Passive Attack (HANDWRITTEN)**

Attacker sees:

```
p, g, X, Y
```

Cannot compute:

```
g^(xy)
```

### ✏️ Explain

* Based on **hard math problem**
* Secure vs eavesdropping

---

# ⚔️ **TASK 11 – MITM Attack (HANDWRITTEN)**

Eve intercepts:

```
X → replaces with XE  
Y → replaces with YE  
```

Result:

```
Alice ↔ Eve (key 1)  
Bob ↔ Eve (key 2)
```

### ✏️ Explain

* Both think they’re secure
* Eve controls communication

---

# 🔄 **TASK 12 – Final Reflection**

### Include:

### Table:

| Method         | Secure? | Problem             |
| -------------- | ------- | ------------------- |
| Public Key     | ❌       | Not authenticated   |
| PKI            | ✅       | Requires trusted CA |
| Diffie-Hellman | ⚠️      | MITM possible       |
| TLS            | ✅       | Combines all        |

### Explain:

* Key distribution is hardest problem
* PKI solves trust
* DH needs authentication
* Session keys improve security

---

# 🏁 **You Now Have**

* ✅ Full lab rebuilt
* ✅ All commands included
* ✅ All required explanations
* ✅ Nothing missing from PDF

---

If you want next, I can:

* Turn this into a **submission-ready PDF template**
* Or split this into **3 individual sections for your group to copy directly**
