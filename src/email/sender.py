"""
Email sending via SendGrid or console preview.
"""

import logging

from src.config import (
    SENDGRID_API_KEY,
    EMAIL_FROM,
    EMAIL_TO,
    EMAIL_PREVIEW_MODE,
)

logger = logging.getLogger(__name__)


def send_email(subject: str, html_content: str, plain_text: str = "") -> bool:
    """
    Send an email via SendGrid, or print to console in preview mode.

    Args:
        subject: Email subject line
        html_content: HTML email body
        plain_text: Plain text fallback (optional)

    Returns:
        True if sent/previewed successfully, False on error
    """
    if EMAIL_PREVIEW_MODE:
        return _preview_email(subject, html_content, plain_text)

    return _send_via_sendgrid(subject, html_content, plain_text)


def _preview_email(subject: str, html_content: str, plain_text: str) -> bool:
    """Print email to console instead of sending."""
    print("\n" + "=" * 70)
    print("EMAIL PREVIEW (not sent)")
    print("=" * 70)
    print(f"From: {EMAIL_FROM or '(not configured)'}")
    print(f"To:   {EMAIL_TO or '(not configured)'}")
    print(f"Subject: {subject}")
    print("-" * 70)
    # Show plain text version for readability in console
    if plain_text:
        print(plain_text)
    else:
        # Strip HTML tags for console display
        import re
        text = re.sub(r"<[^>]+>", "", html_content)
        text = re.sub(r"\n{3,}", "\n\n", text)
        print(text.strip())
    print("=" * 70 + "\n")
    logger.info("Email previewed in console (preview mode enabled)")
    return True


def _send_via_sendgrid(subject: str, html_content: str, plain_text: str) -> bool:
    """Send email through SendGrid API."""
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail, Content

        message = Mail(
            from_email=EMAIL_FROM,
            to_emails=EMAIL_TO,
            subject=subject,
        )
        message.content = [
            Content("text/plain", plain_text or "Please view this email in HTML."),
            Content("text/html", html_content),
        ]

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        if response.status_code in (200, 201, 202):
            logger.info(f"Email sent successfully to {EMAIL_TO} (status: {response.status_code})")
            return True
        else:
            logger.error(f"SendGrid returned status {response.status_code}: {response.body}")
            return False

    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False
