from strands import Agent
from model.load import load_model

agent = Agent(
    model=load_model(),
    system_prompt="You are a DSA code analyzer. Analyze code for correctness, time complexity, and space complexity.",
)

prompt = input("Enter code or question: ")
response = agent(prompt)
print(response)
