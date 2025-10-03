#    !pip install openai-agents
#    !pip install --upgrade openai
from __future__ import annotations

import asyncio
import os

from agents import Agent
from agents import OpenAIChatCompletionsModel
from agents import Runner
from agents import set_tracing_disabled
from load_dotenv import load_dotenv
from openai import AsyncOpenAI

set_tracing_disabled(disabled=True)

load_dotenv()
load_dotenv.load_dotenv()

client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
agent = Agent(
    name="ChatBot",
    instructions="You are a friendly and helpful chatbot. You should provide technical solutions when possible.",
    model=OpenAIChatCompletionsModel(model="gpt-4.1-mini", openai_client=client),
)
print(agent)

while True:
    userInput = input("Ask a question: ")
    if userInput.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break
    result = asyncio.run(Runner.run(agent, userInput))
    print(f'\nChatBot: {result.final_output}\nTo exit, type "exit" or "quit"')
