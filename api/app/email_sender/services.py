import logging
import os
from typing import List, Union
import resend
from pydantic import EmailStr

RESEND_API_KEY = os.getenv("RESEND_API_KEY")


class EmailSender:
    @staticmethod
    async def send_email(
        sender: EmailStr,
        receivers: Union[EmailStr, List[EmailStr]],
        subject: str,
        content: str
    ) -> dict:
        """
        Send an email using the Resend service.
        """
        resend.api_key = RESEND_API_KEY

        try:
            # Convert single receiver to list if necessary
            receiver_list = [receivers] if isinstance(receivers, str) else receivers

            params = {
                "from": sender,
                "to": receiver_list,
                "subject": subject,
                "html": content
            }

            email = resend.Emails.send(params)
            return {"status": "success", "code": 200, "message_id": email.id}
        except Exception as e:
            logging.error("Failed to send email", e.message, e.code)
            return {
                "status": "error",
                "code": e.code,
                "message": f"Failed to send email: {str(e.message)}"
            }