from helpful_agent.app import myAgent_stream
import chainlit as cl

@cl.on_chat_start
async def start_chat():
    await cl.Message(
        content="Welcome to Helpful Assistant! I am a helpful AI Agent created by Rehmat Khalid. How can I assist you today?"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    user_input = message.content

    msg = cl.Message(content="")  # empty placeholder for streaming
    await msg.send()

    try:
        async for chunk in myAgent_stream(user_input):
            await msg.stream_token(chunk)

        await msg.update()
    except Exception as e:
        await cl.Message(content=f"❌ Error: {str(e)}").send()