import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic_settings import BaseSettings
from fastapi import HTTPException
from typing import Type
from pydantic_settings import PydanticBaseSettingsSource


class Settings(BaseSettings):
    # App configurations
    PYTHONUNBUFFERED: int = 1

    # Email configurations
    EMAIL_DOMAIN: str = "gmail.com"
    EMAIL_HOST: str
    EMAIL_PORT: int = 587
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    FROM_EMAIL: str | None = None

    # Kafka configurations
    USE_KAFKA: bool = False
    KAFKA_BOOTSTRAP_SERVERS: str = None
    KAFKA_CONSUMER_TOPIC: str = None
    KAFKA_MESSAGE_KEY: str | None = None

    class Config:
        env_file = ".env"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return dotenv_settings, env_settings, file_secret_settings, init_settings


SETTINGS = Settings()


def send_email(receiver_email: str | list[str], message_text: str, email_object: str):
    # Récupérer les configurations email
    settings = SETTINGS
    EMAIL_DOMAIN = settings.EMAIL_DOMAIN
    EMAIL_HOST = settings.EMAIL_HOST
    EMAIL_PORT = settings.EMAIL_PORT
    EMAIL_USERNAME = settings.EMAIL_USERNAME
    EMAIL_PASSWORD = settings.EMAIL_PASSWORD
    FROM_EMAIL = settings.FROM_EMAIL

    if not all([EMAIL_DOMAIN, EMAIL_HOST, EMAIL_PORT, EMAIL_USERNAME, EMAIL_PASSWORD]):
        print("Email configurations are not properly set.")
        raise HTTPException(
            status_code=400, detail="Email configurations are not properly set."
        )

    # Créer un objet MIMEMultipart pour représenter le message
    from_email = FROM_EMAIL if FROM_EMAIL else f"noreply@{EMAIL_DOMAIN}"
    message = MIMEMultipart()
    message["From"] = from_email

    # receiver_email peut être une chaîne ou une liste; construire la liste
    if isinstance(receiver_email, list):
        recipients_list = receiver_email
        # Header To doit être une string lisible séparée par des virgules
        message["To"] = ", ".join(recipients_list)
    else:
        recipients_list = [receiver_email]
        message["To"] = receiver_email

    message["Subject"] = email_object

    # Créer une partie de message MIMEText pour le corps du message (utf-8)
    # MIMEText attend un texte (str), le third parameter est le charset
    message_body = MIMEText(str(message_text), "html", "utf-8")
    message.attach(message_body)

    try:
        # Créer une session SMTP et envoyer le message
        with smtplib.SMTP(
            EMAIL_HOST,
            EMAIL_PORT,
        ) as server:
            server.starttls()
            server.login(
                user=EMAIL_USERNAME,
                password=EMAIL_PASSWORD,
            )
            # sendmail accepte une liste de destinataires
            server.sendmail(from_email, recipients_list, message.as_string())
            print(f"Email sent to {recipients_list}")
            return True
    except Exception as e:
        print(f"Error, unable to send email {e}")
        raise HTTPException(status_code=400, detail=f"Error sending email: {e}")


def get_smtp_server_status() -> bool:
    settings = SETTINGS
    EMAIL_HOST = settings.EMAIL_HOST
    EMAIL_PORT = settings.EMAIL_PORT
    EMAIL_USERNAME = settings.EMAIL_USERNAME
    EMAIL_PASSWORD = settings.EMAIL_PASSWORD

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=10) as server:
            server.starttls()
            server.login(user=EMAIL_USERNAME, password=EMAIL_PASSWORD)
            server.noop()
            return True
    except Exception as e:
        print(f"SMTP server connection failed: {e}")
        raise e
