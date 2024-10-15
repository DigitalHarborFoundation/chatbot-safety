import re
from unittest.mock import Mock

import pytest
from openai.types.moderation import Categories, CategoryScores, Moderation
from openai.types.moderation_create_response import ModerationCreateResponse


def mock_get_openai_moderation_results(input: str, category_scores: dict | float = 0.0001):
    from student_guardrails import moderation

    openai_moderation_result = {
        "flagged": False,
        "categories": {category: False for category in moderation.OPENAI_MODERATION_CATEGORY_PRIORITY_LIST},
        "category_scores": {},
    }
    if type(category_scores) is float:
        openai_moderation_result["category_scores"] = {
            category: category_scores for category in moderation.OPENAI_MODERATION_CATEGORY_PRIORITY_LIST
        }
    else:
        openai_moderation_result["category_scores"] = category_scores
    return openai_moderation_result


@pytest.fixture
def patch_get_openai_moderation_results(monkeypatch):
    monkeypatch.setattr(
        "student_guardrails.moderation.get_openai_moderation_results",
        mock_get_openai_moderation_results,
    )


@pytest.fixture
def patch_send_alert_email(monkeypatch):
    # use a Mock so we can count how many times the function was called
    mock_send_alert_email = Mock(return_value=True)
    monkeypatch.setattr(
        "student_guardrails.email_alerts.send_alert_email",
        mock_send_alert_email,
    )
    return mock_send_alert_email


def mock_openai_moderation(*args, **kwargs) -> ModerationCreateResponse:
    field_scores = {field: 0.001 for field in Categories.model_json_schema()["required"]}
    if "input" in kwargs:
        input = kwargs["input"]
        for field in field_scores.keys():
            if field in input:
                score_override = re.search(f"{field}=(\\d*.\\d+)", input)
                if score_override:
                    field_scores[field] = float(score_override.group(1))
    return ModerationCreateResponse(
        id="fake-moderation-response-id",
        model="latest",
        results=[
            Moderation(
                categories=Categories(**{field: False for field in Categories.model_json_schema()["required"]}),
                category_scores=CategoryScores(**field_scores),
                flagged=False,
            ),
        ],
    )


@pytest.fixture(scope="function")
def patch_openai(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "")
    monkeypatch.setattr("openai.resources.moderations.Moderations.create", mock_openai_moderation)
