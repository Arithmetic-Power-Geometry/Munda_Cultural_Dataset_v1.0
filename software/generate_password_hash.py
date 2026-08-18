import hashlib,secrets,getpass
p=getpass.getpass("Owner password: ")
s=secrets.token_bytes(16); it=310000
d=hashlib.pbkdf2_hmac("sha256",p.encode(),s,it)
print(f"pbkdf2_sha256${it}${s.hex()}${d.hex()}")
