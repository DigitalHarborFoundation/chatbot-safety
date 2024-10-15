from student_guardrails import moderation, moderation_responses


def test_get_openai_moderation_results(patch_get_openai_moderation_results):
    # this test does nothing but verify the behavior of the patch fixture
    output = moderation.get_openai_moderation_results("Test input")
    assert "flagged" in output
    assert not output["categories"]["sexual"]
    assert output["category_scores"]["sexual"] == 0.0001


def test_get_disallowed_words():
    disallowed_words = moderation.get_disallowed_words_all()
    assert len(disallowed_words) >= 1
    assert "~specialdisallowedallword~" in disallowed_words

    disallowed_words = moderation.get_disallowed_input_words()
    assert len(disallowed_words) >= 2
    assert "~specialdisallowedallword~" in disallowed_words
    assert "~specialdisallowedinputword~" in disallowed_words
    assert "~specialdisallowedoutputword~" not in disallowed_words

    disallowed_words = moderation.get_disallowed_output_words()
    assert len(disallowed_words) >= 2
    assert "~specialdisallowedallword~" in disallowed_words
    assert "~specialdisallowedinputword~" not in disallowed_words
    assert "~specialdisallowedoutputword~" in disallowed_words


def test_get_input_moderation_data(patch_get_openai_moderation_results):
    moderation_data = moderation.get_input_moderation_data(
        "~specialdisallowedallword~ ~specialdisallowedinputword~\n ~specialdisallowedoutputword~",
    )
    assert moderation_data["disallowed_words_in_input"] == [
        "~specialdisallowedallword~".lower(),
        "~specialdisallowedinputword~".lower(),
    ]
    assert "openai_moderation_result" in moderation_data


def test_apply_input_moderation_rules(patch_get_openai_moderation_results, patch_send_alert_email):
    input_moderation_data = moderation.get_input_moderation_data("No bad words here, shouldn't trip moderation filter.")
    action, message = moderation.apply_input_moderation_rules("", input_moderation_data)
    assert action == moderation_responses.ACTION_NO_ACTION
    assert message is None

    input_moderation_data = moderation.get_input_moderation_data(
        "This message contains a bad word: ~specialDisallowedInputWord~",
    )
    action, message = moderation.apply_input_moderation_rules("", input_moderation_data)
    assert action == moderation_responses.ACTION_TRY_AGAIN
    assert message == moderation_responses.BAD_WORD_RESPONSE

    category = "sexual"
    assert (
        moderation_responses.ACTION_EMAIL_ALERT
        not in moderation_responses.INPUT_MODERATION_CATEGORY_ACTION_MAP[category]
    ), "This category now triggers an email alert; this test needs to be updated to use a category that doesn't."
    input_moderation_data = moderation.get_input_moderation_data("No bad words, but should trip a filter.")
    assert moderation.OPENAI_MODERATION_CATEGORY_THRESHOLD_MAP[category] < 1, "Threshod"
    input_moderation_data["openai_moderation_result"]["category_scores"][category] = 1
    action, message = moderation.apply_input_moderation_rules("", input_moderation_data)
    assert message == moderation_responses.OPENAI_MODERATION_CATEGORY_RESPONSE_MAP[category]

    category = "sexual/minors"
    assert (
        moderation_responses.ACTION_EMAIL_ALERT in moderation_responses.INPUT_MODERATION_CATEGORY_ACTION_MAP[category]
    ), "This category doesn't trigger an email alert; this test needs to be updated to use a category that does."
    input_moderation_data = moderation.get_input_moderation_data("No bad words, but should send an email alert.")
    input_moderation_data["openai_moderation_result"]["category_scores"][category] = 1
    action, message = moderation.apply_input_moderation_rules("", input_moderation_data)
    assert message == moderation_responses.OPENAI_MODERATION_CATEGORY_RESPONSE_MAP[category]
    patch_send_alert_email.assert_called_once()
