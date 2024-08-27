from openai import AsyncOpenAI
import chainlit as cl

# Set up the AsyncOpenAI client with the base URL and API key
client = AsyncOpenAI(base_url="http://localhost:8080/v1", api_key="fake-key")

# Instrument the OpenAI client for monitoring purposes
cl.instrument_openai()

# Define settings for the model's behavior
settings = {
    "model": "llama3.1-8b",
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

@cl.on_chat_start
def start_chat():
    """
    Initializes the chat session by setting a system message in the user's session.
    """
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )

@cl.on_message
async def main(message: cl.Message):
    """
    Handles incoming user messages, sends them to the language model, and streams the response back.
    """
    # Retrieve the current message history from the user session
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    # Initialize a message object to manage the response
    msg = cl.Message(content="")
    await msg.send()  # Send an empty message to indicate the response has started

    # Create a chat completion stream using the message history and settings
    stream = await client.chat.completions.create(
        messages=message_history, stream=True, **settings
    )

    # Stream each token of the response back to the user
    async for part in stream:
        token = part.choices[0].delta.content or ""
        if token:
            await msg.stream_token(token)

    # Update the message history with the assistant's complete response
    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()  # Update the message with the complete content
