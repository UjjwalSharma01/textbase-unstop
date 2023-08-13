import textbase
from textbase.message import Message
from textbase import models
from typing import List

# Load your OpenAI API key
models.OpenAI.api_key = "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"

# Introductory message for language learning
SYSTEM_PROMPT = """Welcome to the Spanish Language Learning Adventure! You're about to embark on an exciting journey to learn Spanish using English. Start by asking questions or practicing simple sentences. ¡Vamos a aprender juntos!
"""

# Stateful information to track progress and vocabulary
user_state = {"level": 1, "vocabulary": {}}

@textbase.chatbot("spanish-learning-bot")
def on_message(message_history: List[Message], state: dict = None):
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """

    # Initialize bot response
    bot_response = ""

    # Check if state is None or if user is starting a new conversation
    if state is None or state.get("new_conversation", False):
        bot_response = SYSTEM_PROMPT
        new_state = {"new_conversation": False}
    else:
        # Retrieve user's last message
        user_message = message_history[-1].text.lower()

        # Implement language learning logic
        if "learn" in user_message:
            # Extract English input
            english_input = user_message.replace("learn", "").strip()

            # Use GPT-3.5 Turbo to generate Spanish response
            spanish_response = models.OpenAI.generate(
                system_prompt=SYSTEM_PROMPT,
                message_history=message_history,
                model="gpt-3.5-turbo",
            )

            # Store learned vocabulary in state
            user_state["vocabulary"][english_input] = spanish_response

            # Update user's level based on progress
            # You can implement logic to increase the level as vocabulary grows

            # Compose response
            bot_response = f"You've learned '{english_input}' in Spanish: {spanish_response}"

        # Add more logic for language learning interactions

        # Update state
        new_state = state

    return bot_response, new_state
