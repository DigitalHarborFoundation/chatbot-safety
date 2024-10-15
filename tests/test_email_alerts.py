from unittest.mock import Mock

from student_guardrails import email_alerts


def test_send_alert_email(monkeypatch):
    # confirm that an email is not sent when the API key is not provided
    monkeypatch.setattr("student_guardrails.email_alerts.SENDGRID_API_KEY", None)
    assert not email_alerts.send_alert_email("TestSubject", "TestContent")

    # and when there are no recipients
    monkeypatch.setattr("student_guardrails.email_alerts.SENDGRID_API_KEY", "fake-api-key")
    monkeypatch.setattr("student_guardrails.email_alerts.ALERT_EMAIL_RECIPIENTS", [])
    assert not email_alerts.send_alert_email("TestSubject", "TestContent")

    # verify that the API is called
    monkeypatch.setattr(
        "student_guardrails.email_alerts.ALERT_EMAIL_RECIPIENTS",
        [
            "test@example.com",
        ],
    )
    response_mock = Mock(status_code=200)
    api_object_mock = Mock(
        spec=email_alerts.SendGridAPIClient,
        **{"send.return_value": response_mock},
    )
    api_mock = Mock(return_value=api_object_mock)
    monkeypatch.setattr(
        "student_guardrails.email_alerts.SendGridAPIClient",
        api_mock,
    )
    assert email_alerts.send_alert_email("TestSubject", "TestContent")
    api_mock.assert_called_once()
    api_object_mock.send.assert_called_once()
    # TODO could inspect the Mail to api_mock's send() method, verifying that all of rori_generative_api.config.ALERT_EMAIL_RECIPIENTS are in the to field
