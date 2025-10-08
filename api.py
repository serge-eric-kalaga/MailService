from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils import send_email, get_smtp_server_status


router = APIRouter()


class EmailRequest(BaseModel):
    receiver_email: str | list[str] = Body(
        ...,
        description="Email address(es) of the receiver(s) - can be a single email or a list of emails",
    )
    email_object: str = Body(default="No Subject", description="Subject of the email")
    message_text: str = Body(..., description="Content of the email")


class ServerStatusResponse(BaseModel):
    status: bool
    message: str


@router.post("/send-email")
async def send_email_endpoint(email_request: EmailRequest):
    """
    Endpoint to send an email.
    - **receiver_email**: Email address(es) of the receiver(s) - can be a single email or a list of emails
    - **email_object**: Subject of the email
    - **message_text**: Content of the email
    Returns a success message if the email is sent successfully, otherwise raises an HTTPException.
    """

    # Validate receiver_email but keep its original type (str or list[str])
    if isinstance(email_request.receiver_email, list):
        if not all(
            isinstance(email, str) and "@" in email
            for email in email_request.receiver_email
        ):
            raise HTTPException(
                status_code=400, detail="Invalid email address in the list"
            )
        recipients = email_request.receiver_email
    elif (
        isinstance(email_request.receiver_email, str)
        and "@" in email_request.receiver_email
    ):
        recipients = email_request.receiver_email
    else:
        raise HTTPException(status_code=400, detail="Invalid email address")

    success = send_email(
        receiver_email=recipients,
        message_text=email_request.message_text,
        email_object=email_request.email_object,
    )
    if not success:
        raise HTTPException(status_code=500, detail="Error sending email")
    return JSONResponse(content={"message": "Email sent successfully"})


@router.get("/smtp-status", response_model=ServerStatusResponse)
async def smtp_status():
    """
    Endpoint to check the status of the SMTP server.
    Returns a message indicating whether the SMTP server is reachable or not.
    """
    try:
        status = get_smtp_server_status()
        message = (
            "SMTP server is reachable." if status else "SMTP server is not reachable."
        )
        return ServerStatusResponse(status=status, message=message)
    except Exception as e:
        message = f"Error checking SMTP server status: {e}"
        return ServerStatusResponse(status=False, message=message)
