import json
import logging
import os
from datetime import datetime, timezone

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)


DATA_DASHBOARD_BASE_URL = "https://localhost/"
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
ALERT_EMAIL_SENDER = os.environ.get("ALERT_EMAIL_SENDER", "moderation-alerts@example.com")
ALERT_EMAIL_RECIPIENTS = "example@example.com,example2@example.com"


def create_alert_email(moderation_data: dict) -> tuple[str, str]:
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    input_message = moderation_data.pop("input_message", "")
    category = moderation_data.pop("category", "unknown")
    subject = f"Rori moderation alert: {category} ({date_str})"

    url = DATA_DASHBOARD_BASE_URL + "/Public_Line"
    activity_session_id = moderation_data.pop("activity_session_id", "")
    query_params = (
        f"?menu_index=4&gdwi=0&gf0column=message__activity_session__id&gf0value={activity_session_id}&gf0function="
    )
    delvin_url = url + query_params

    input_moderation_data_str = json.dumps(moderation_data.pop("input_moderation_data", {}), indent=2).replace(
        "\n",
        "<br>&nbsp;",
    )

    try:
        other_metadata_str = json.dumps(moderation_data, indent=2).replace("\n", "<br>&nbsp;")
    except (TypeError, OverflowError):
        logger.error("Failed to JSON serialize remaining metadata: {moderation_data}")
        other_metadata_str = (
            f"Metadata contained a value that couldn't be serialized to JSON. Keys: {list(moderation_data.keys())}"
        )
    content = (
        f"Category: {category}"
        "<br><br>"
        f'Message that triggered the alert: "{input_message}"'
        "<br><br>"
        f"Time of alert (UTC): {datetime.now(timezone.utc).isoformat()}"
        "<br><br>"
        f"View in the Rori data dashboard: {delvin_url}<br><br>"
        f"Moderation metadata: {input_moderation_data_str}<br><br>"
        f"Other metadata: {other_metadata_str}<br>"
    )
    return subject, content


def send_alert_email(subject: str, content: str) -> bool:
    if not SENDGRID_API_KEY or len(ALERT_EMAIL_RECIPIENTS) == 0:
        logger.warning(
            f"Would have sent alert email, but configuration invalid. Configured recipients: {ALERT_EMAIL_RECIPIENTS}",
        )
        return False
    message = Mail(
        from_email=ALERT_EMAIL_SENDER,
        to_emails=ALERT_EMAIL_RECIPIENTS,
        subject=subject,
        html_content=content,
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        if response.status_code >= 200 and response.status_code < 300:
            logger.info(f"Successfully sent alert email, receiving status code {response.status_code}.")
        else:
            logger.error(f"Failed to send alert email, receiving status code {response.status_code}.")
        return True
    except Exception as e:
        raise e
