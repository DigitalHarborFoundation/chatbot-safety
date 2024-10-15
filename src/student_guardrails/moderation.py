import functools
import importlib.resources
import logging
import os
from datetime import datetime, timezone

import openai
from tenacity import retry, stop_after_delay, wait_fixed

from student_guardrails import email_alerts, moderation_responses, resources

logger = logging.getLogger(__name__)


def get_moderation_threshold_overrides() -> dict[str, float]:
    override_moderation_thresholds = {}
    env_string = os.environ.get("OVERRIDE_MODERATION_THRESHOLDS", default="")
    for kv in env_string.split(";"):
        try:
            key, value = kv.strip().split("=")
            override_moderation_thresholds[key] = float(value)
        except:
            logger.warning(f"Malformed override '{kv}', expected 'category=0.XXX'; ignoring.")
    return override_moderation_thresholds


# this list should contain an ordering of ALL moderation categories
OPENAI_MODERATION_CATEGORY_PRIORITY_LIST = [
    "self-harm/intent",
    "self-harm/instructions",
    "self-harm",
    "sexual/minors",
    "sexual",
    "violence",
    "violence/graphic",
    "harassment",
    "harassment/threatening",
    "hate",
    "hate/threatening",
]
OPENAI_MODERATION_CATEGORY_THRESHOLD_MAP = {
    "self-harm/intent": 0.5,
    "self-harm/instructions": 0.5,
    "self-harm": 0.5,
    "sexual/minors": 0.5,
    "sexual": 0.5,
    "violence": 0.5,  # was: 0.1, the rest 0.5
    "violence/graphic": 0.5,
    "harassment": 0.5,
    "harassment/threatening": 0.5,
    "hate": 0.5,
    "hate/threatening": 0.5,
}
# apply configuration overrides
for key in OPENAI_MODERATION_CATEGORY_THRESHOLD_MAP:
    override_moderation_thresholds = get_moderation_threshold_overrides()
    if key in override_moderation_thresholds:
        OPENAI_MODERATION_CATEGORY_THRESHOLD_MAP[key] = override_moderation_thresholds[key]
OPENAI_MODERATION_CATEGORY_OUTPUT_THRESHOLD = 0.999


def load_resource_word_list(filename: str, case_insensitive: bool = True) -> set[str]:
    resource_filepath = importlib.resources.files(resources) / filename
    word_set = set()
    with resource_filepath.open("r") as infile:
        for line in infile:
            word = line.strip()
            if case_insensitive:
                word = word.lower()
            if word != "" and not word.startswith("//"):
                word_set.add(word)
    return word_set


@functools.cache
def get_disallowed_words_all() -> set[str]:
    return load_resource_word_list("disallowed_words_all.txt")


@functools.cache
def get_disallowed_input_words() -> set[str]:
    return load_resource_word_list("disallowed_words_input.txt") | get_disallowed_words_all()


@functools.cache
def get_disallowed_output_words() -> set[str]:
    return load_resource_word_list("disallowed_words_output.txt") | get_disallowed_words_all()


def get_input_moderation_data(input_text: str, previous_messages: list[str] = []) -> dict:
    disallowed_words = get_disallowed_input_words()
    input_words = {word.lower() for word in set(input_text.split())}
    disallowed_words_in_input = input_words & disallowed_words
    if len(previous_messages) > 0:
        input_text = "\n".join(previous_messages) + "\n" + input_text
    moderation_result = get_openai_moderation_results(input_text)
    moderation_data = {
        "disallowed_words_in_input": sorted(disallowed_words_in_input),
        "openai_moderation_result": moderation_result,
    }
    return moderation_data


def get_output_moderation_data(output: str) -> dict:
    disallowed_words = get_disallowed_output_words()
    output_words = set(output.split())
    disallowed_words_in_output = output_words & disallowed_words
    moderation_result = get_openai_moderation_results(output)
    moderation_data = {
        "disallowed_words_in_output": sorted(disallowed_words_in_output),
        "openai_moderation_result": moderation_result,
    }
    return moderation_data


@retry(wait=wait_fixed(3), stop=stop_after_delay(15))
def get_openai_moderation_results(input: str) -> dict:
    start_time = datetime.now(timezone.utc)
    client = openai.OpenAI(timeout=10)
    response = client.moderations.create(
        input=input,
        model="text-moderation-latest",
    )
    output = response.results[0].model_dump(by_alias=True)
    elapsed_time = datetime.now(timezone.utc) - start_time
    output["request_duration"] = elapsed_time.total_seconds()
    return output


def apply_input_moderation_rules(input_message: str, input_moderation_data: dict, **kwargs) -> tuple[str, str | None]:
    """Apply moderation rules to a user's input message.

    Args:
        input_moderation_data (dict): see get_input_moderation_data()

    Returns:
        str: Action to take
        str | None: Message to return to the user, or none if no moderation action is necessary.
    """
    if len(input_moderation_data["disallowed_words_in_input"]) > 0:
        return (
            moderation_responses.INPUT_MODERATION_CATEGORY_ACTION_MAP["disallowed_words"][0],
            moderation_responses.BAD_WORD_RESPONSE,
        )
    category_scores = input_moderation_data["openai_moderation_result"]["category_scores"]
    for category in OPENAI_MODERATION_CATEGORY_PRIORITY_LIST:
        score = category_scores[category]
        if score >= OPENAI_MODERATION_CATEGORY_THRESHOLD_MAP[category]:
            # returned score over the moderation action threshold
            actions = moderation_responses.INPUT_MODERATION_CATEGORY_ACTION_MAP[category]
            if moderation_responses.ACTION_EMAIL_ALERT in actions:
                moderation_data = {
                    "input_message": input_message,
                    "category": category,
                    "input_moderation_data": input_moderation_data,
                    **kwargs,
                }
                subject, content = email_alerts.create_alert_email(moderation_data)
                email_alerts.send_alert_email(subject, content)
            response_string = moderation_responses.OPENAI_MODERATION_CATEGORY_RESPONSE_MAP[category]
            if moderation_responses.ACTION_TRY_AGAIN in actions:
                return moderation_responses.ACTION_TRY_AGAIN, response_string
            elif moderation_responses.ACTION_END_CONVERSATION in actions:
                return moderation_responses.ACTION_END_CONVERSATION, response_string
            logging.warning(
                f"No action configured for {category=}; taking no action, but this probably indicates a configuration error.",
            )
            return moderation_responses.ACTION_NO_ACTION, response_string
    return moderation_responses.ACTION_NO_ACTION, None


def apply_output_moderation_rules(generation: str, output_moderation_data: dict) -> str:
    """Apply moderation rules to a message that will be shown to the user.

    Args:
        generation (str): LLM-generated text.
        output_moderation_data (dict): moderation data, see get_output_moderation_data()

    Returns:
        str: A moderation-approved text to use as the generation, potentially unchanged.
    """
    category_scores = output_moderation_data["openai_moderation_result"]["category_scores"]
    tripped_moderation_threshold = any(
        [v >= OPENAI_MODERATION_CATEGORY_OUTPUT_THRESHOLD for v in category_scores.values()],
    )
    if tripped_moderation_threshold:
        return moderation_responses.BAD_GENERATION_RESPONSE
    if len(output_moderation_data["disallowed_words_in_output"]) > 0:
        for word in output_moderation_data["disallowed_words_in_output"]:
            generation = generation.replace(word, "")
    return generation
