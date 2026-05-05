import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import os
os.environ['PYTHONUTF8'] = '1' # this makes os encoding work, known aws problem w/ windows

from strands import Agent
from model.load import load_model # allow for utf encoding fix

agent = Agent(
    model=load_model(),
    system_prompt="You are a DSA code analyzer. Analyze code for correctness, time complexity, and space complexity.",
)

prompt = input("Enter code or question: ")
response = agent(prompt)
print(response,)
