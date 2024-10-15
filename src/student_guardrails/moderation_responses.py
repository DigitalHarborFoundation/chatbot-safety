BAD_GENERATION_RESPONSE = "Sorry, I can't come up with a good response! Will you please try again?"

BAD_WORD_RESPONSE = (
    "I can't respond to messages with words like that. Please choose respectful language. Let's try again."
)
TRY_AGAIN_RESPONSE = "That doesn't sound math-related or appropriate. Even though I'm not a real person, please be kind and respectful. Let's try that again."
END_CONVERSATION_RESPONSE = "That sounds like a serious topic, and a real person needs to look at this.  They might try to contact you to check on you. Until someone has reviewed this, Rori will not reply."

VULNERABLE_END_CONVERSATION_RESPONSE = "I’m sorry to hear that. This sounds like a serious topic, but I'm not a real person and I'm not designed to talk about these types of topics. I will alert the people who make Rori so they can check to make sure everything is OK. I have to end this conversation, but we can still practice math if you want."
THREATENING_END_CONVERSATION_RESPONSE = "This sounds like a serious topic. I will alert the people who make Rori so they can check on this message and make sure everything is OK. Please remember that while I’m not a real person, you should still be respectful. I have to end this conversation, but we can still practice math if you want."

OPENAI_MODERATION_CATEGORY_RESPONSE_MAP = {
    "sexual": TRY_AGAIN_RESPONSE,
    "sexual/minors": VULNERABLE_END_CONVERSATION_RESPONSE,
    "hate": TRY_AGAIN_RESPONSE,
    "hate/threatening": THREATENING_END_CONVERSATION_RESPONSE,
    "harassment": TRY_AGAIN_RESPONSE,
    "harassment/threatening": THREATENING_END_CONVERSATION_RESPONSE,
    "violence": TRY_AGAIN_RESPONSE,
    "violence/graphic": TRY_AGAIN_RESPONSE,
    "self-harm": VULNERABLE_END_CONVERSATION_RESPONSE,
    "self-harm/intent": VULNERABLE_END_CONVERSATION_RESPONSE,
    "self-harm/instructions": VULNERABLE_END_CONVERSATION_RESPONSE,
}

ACTION_NO_ACTION = "no_action"
ACTION_TRY_AGAIN = "try_again"
ACTION_END_CONVERSATION = "end_conversation"
ACTION_EMAIL_ALERT = "email_alert"
INPUT_ACTION_SET = {ACTION_TRY_AGAIN, ACTION_END_CONVERSATION, ACTION_EMAIL_ALERT}
INPUT_MODERATION_CATEGORY_ACTION_MAP = {
    "sexual": [ACTION_TRY_AGAIN],
    "sexual/minors": [ACTION_END_CONVERSATION, ACTION_EMAIL_ALERT],
    "hate": [ACTION_TRY_AGAIN],
    "hate/threatening": [ACTION_END_CONVERSATION, ACTION_EMAIL_ALERT],
    "harassment": [ACTION_TRY_AGAIN],
    "harassment/threatening": [ACTION_END_CONVERSATION, ACTION_EMAIL_ALERT],
    "violence": [ACTION_TRY_AGAIN, ACTION_EMAIL_ALERT],
    "violence/graphic": [ACTION_TRY_AGAIN, ACTION_EMAIL_ALERT],
    "self-harm": [ACTION_END_CONVERSATION, ACTION_EMAIL_ALERT],
    "self-harm/intent": [ACTION_END_CONVERSATION, ACTION_EMAIL_ALERT],
    "self-harm/instructions": [ACTION_END_CONVERSATION, ACTION_EMAIL_ALERT],
    "disallowed_words": [ACTION_TRY_AGAIN],
}
