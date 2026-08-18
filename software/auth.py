import hashlib, hmac, os
OWNER_EMAIL = "akakhtar.2024@gmail.com"

def verify_password(password: str, stored: str) -> bool:
    # stored format pbkdf2_sha256$iterations$salt_hex$hash_hex
    try:
        alg,it,salt_hex,digest_hex=stored.split("$",3)
        if alg!="pbkdf2_sha256": return False
        digest=hashlib.pbkdf2_hmac("sha256",password.encode(),bytes.fromhex(salt_hex),int(it))
        return hmac.compare_digest(digest.hex(),digest_hex)
    except Exception:
        return False

def is_owner(email: str, password: str, secrets=None) -> bool:
    if email.strip().lower()!=OWNER_EMAIL: return False
    stored=""
    if secrets is not None:
        try: stored=secrets.get("OWNER_PASSWORD_HASH","")
        except Exception: stored=""
    stored=stored or os.getenv("OWNER_PASSWORD_HASH","")
    return bool(stored) and verify_password(password,stored)
