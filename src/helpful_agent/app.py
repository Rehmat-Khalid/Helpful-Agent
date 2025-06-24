from dotenv import load_dotenv
import os
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled

load_dotenv()
set_tracing_disabled(True)

# Load from .env
api_key = os.getenv("GOOGLE_API_KEY")
base_url = os.getenv("GOOGLE_BASE_URL")
model_name = os.getenv("GOOGLE_MODEL")

provider = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
)

model = OpenAIChatCompletionsModel(
    model=model_name,
    openai_client=provider
)

async def myAgent_stream(user_input):
    Agent1 = Agent(
        name="Helpful Assistant",
        instructions="A helpful assistant that can answer every question and provide information.",
        model=model 
    )

    try:
        # Actual streaming method
        async for step in Runner.run_stream(Agent1, user_input):
            if step.output is not None:
                yield step.output

    except AttributeError:
        # Fallback if run_stream is not available
        print("⚠️ run_stream not found, using fallback.")
        response = await Runner.run(Agent1, user_input)
        text = response.final_output
        for word in text.split(" "):
            yield word + " "