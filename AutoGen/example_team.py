from dotenv import load_dotenv
import os
import asyncio

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage
from autogen_core.tools import FunctionTool

load_dotenv()
GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI API Key is not pres")

llm_client = OpenAIChatCompletionClient(model='gemini-2.5-flash',api_key=GEMINI_API_KEY)

myAssistantAgent = AssistantAgent(
    name = "PoetryAssistance",
    description="An assistant agent that help to write poem",
    model_client= llm_client,
    system_message="You're helpful assistance agent who can write poetry only"
)

myUserAgent = UserProxyAgent(
    name= "MyUserAgent",
    description="A user proxy agent that act as user",
    input_func=input
)

termination_call = TextMentionTermination("exit")

"""Round-Robin team"""
team = RoundRobinGroupChat(
    participants=[myAssistantAgent,myUserAgent],
    termination_condition=termination_call
)

stream = team.run_stream(task="Write a 4 line poem about nature")

async def main():
    await Console(stream)

if __name__ == '__main__':
    asyncio.run(main())
