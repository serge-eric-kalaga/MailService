import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic_settings import BaseSettings
from fastapi import HTTPException
from typing import Type
from pydantic_settings import PydanticBaseSettingsSource


class Settings(BaseSettings):
    EMAIL_DOMAIN: str
    EMAIL_HOST: str
    EMAIL_PORT: int = 587
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    FROM_EMAIL: str | None = None

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
    message["To"] = receiver_email
    message["Subject"] = email_object

    # Créer une partie de message MIMEText pour le corps du message
    message_body = MIMEText(str(message_text).encode("utf-8"), "html", "utf-8")
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
            server.sendmail(from_email, receiver_email, message.as_string())
            print(f"Email sent to {receiver_email}")
            return True
    except Exception as e:
        print(f"Error, unable to send email {e}")
        raise HTTPException(status_code=500, detail=f"Error sending email: {e}")
