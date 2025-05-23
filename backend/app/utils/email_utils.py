from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os
from dotenv import load_dotenv
from datetime import datetime
from app.database import users_collection

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS") == "True",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS") == "True",
    USE_CREDENTIALS=True
)

async def send_verification_email(email_to: str, token: str):
    link = f"http://localhost:8000/auth/verify-email?token={token}"
    message = MessageSchema(
        subject="Vérification de votre adresse email",
        recipients=[email_to],
        body=f"Bonjour,\n\nMerci pour votre inscription !\nCliquez ici pour vérifier votre adresse : {link}",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)

async def send_info_email(to_email: str, subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[to_email],
        body=body,
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)

def log_user_activity(email: str, action: str):
    users_collection.update_one(
        {"email": email},
        {"$push": {
            "activity_log": {
                "action": action,
                "timestamp": datetime.utcnow()
            }
        }}
    )