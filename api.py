from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils import send_email


class EmailRequest(BaseModel):
    receiver_email: str | list[str]
    message_text: str
    email_object: str


router = APIRouter()


@router.post("/send-email")
async def send_email_endpoint(email_request: EmailRequest):
    success = send_email(
        receiver_email=email_request.receiver_email,
        message_text=email_request.message_text,
        email_object=email_request.email_object,
    )
    if not success:
        raise HTTPException(status_code=500, detail="Error sending email")
    return JSONResponse(content={"message": "Email sent successfully"})
