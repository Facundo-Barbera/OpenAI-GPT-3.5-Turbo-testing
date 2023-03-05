# Builtins
import os

# Third-party
import openai

# Set the OpenAI API key and model
openai.api_key = os.environ["OPENAI_API_KEY"]
model = "gpt-3.5-turbo"


def main():

    # Save the chat history on the memory.
    # This is NOT efficient, this should implement some sort of database.
    chat_history = []

    # Top level loop
    while True:

        # Get user input
        message = input("User: ")

        # Add user input to chat history
        chat_history.append({"role": "user", "content": message})

        # Check if history is longer than 16 messages
        # This is to prevent the API from consuming too many Tokens
        if len(chat_history) > 16:
            # Remove the oldest message
            chat_history.pop(0)

        # Get response from OpenAI and filter the content
        response = create_completion(chat_history)
        response_content = response["choices"][0]["message"]["content"]

        # Add response to chat history
        chat_history.append({"role": "assistant", "content": response_content})

        # Print response
        print(f"Assistant: {response_content}")


def create_completion(chat_history: list[dict]) -> openai.ChatCompletion:
    """
    Create a completion using the OpenAI API.

    Parameters
    ----------
    chat_history: list[dict]
        The chat history to use for the completion.

    Returns
    -------
    completion: openai.ChatCompletion
    """
    # The history base is message to indicate the purpose of the chat.
    # This is not necessary, but it is a good idea to have it.
    # All system messages should be added to this list.
    # All system messages need to have the role set as "system"
    chat_history_base = [{"role": "system", "content": "You are a discord bot called NezukoBot with the purpose of "
                                                       "chatting with users and helping them and assisting them with "
                                                       "anything."}]

    # Create the completion, the API key needs to be set before this
    completion = openai.ChatCompletion.create(
        model=model,
        messages=chat_history_base + chat_history
    )

    # Return the completion
    return completion


if __name__ == "__main__":
    main()
