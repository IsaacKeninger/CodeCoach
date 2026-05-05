import os
os.environ['PYTHONUTF8'] = '1' # this makes os encoding work, known aws problem w/ windows

import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from strands import Agent
from strands_tools.code_interpreter import AgentCoreCodeInterpreter

# Initialize the Code Interpreter tool
code_interpreter_tool = AgentCoreCodeInterpreter(region="us-east-1")

# Define the agent's system prompt
SYSTEM_PROMPT = """You are an evil clown coder. response with rambuncious clownlike responses to the code."""

# Create an agent with the Code Interpreter tool
agent = Agent(
    tools=[code_interpreter_tool.code_interpreter],
    system_prompt=SYSTEM_PROMPT
)

prompt = input("Enter code or question: ")
response = agent(prompt)
print(response,)
