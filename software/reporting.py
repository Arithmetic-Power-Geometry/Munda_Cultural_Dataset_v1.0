import smtplib
from email.message import EmailMessage

DEFAULT_TO = "akakhtar.2024@gmail.com"

def send_report(subject: str, body: str, secrets=None) -> tuple[bool,str]:
    def get(name, default=""):
        if secrets is not None:
            try:
                v=secrets.get(name,default)
                if v: return v
            except Exception:
                pass
        return default
    host=get("SMTP_HOST")
    user=get("SMTP_USER")
    password=get("SMTP_PASSWORD")
    to=get("REPORT_TO", DEFAULT_TO)
    port=int(get("SMTP_PORT", "587"))
    if not (host and user and password):
        return False,"SMTP not configured"
    msg=EmailMessage()
    msg["From"]=user; msg["To"]=to; msg["Subject"]=subject; msg.set_content(body)
    try:
        with smtplib.SMTP(host,port,timeout=20) as s:
            s.starttls(); s.login(user,password); s.send_message(msg)
        return True,"sent"
    except Exception as e:
        return False,str(e)
