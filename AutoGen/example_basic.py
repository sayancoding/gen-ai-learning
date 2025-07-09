from dotenv import load_dotenv
import os
import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage
from autogen_core.tools import FunctionTool

load_dotenv()
GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI API Key is not pres")

llm_client = OpenAIChatCompletionClient(model='gemini-2.5-flash',api_key=GEMINI_API_KEY)

def reverse_string(text:str)->str:
    """Reverse function for String"""
    return text[::-1]

"""Creating a tool that use above function for operation"""
reverse_tool = FunctionTool(reverse_string, "A tool to reserve a string")

"""Assistant-Agent : responsible to do the job using help of functionTools"""
myAgent = AssistantAgent(
    name= "StringAgent",
    model_client= llm_client,
    system_message="You're assistance agent to help to reverse a String using help of reverse_tool",
    tools=[reverse_tool]
)

task = "Reverse the text 'This is computer'"

async def main():
    response = await myAgent.run(task=task)
    print(f"Agent response :: {response}")
    await llm_client.close()

if __name__ == "__main__":
    asyncio.run(main())
