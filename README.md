** Project Idea **
An agentic AI tool, CodeCoach recives DSA/Leetcode Style code responses from the user and provides memory integrated
hints, responses, and solutions in a converstional manner to the user. Instead of just an LLM giving a response to code, 
CodeCoach's agent statefully tracks and acts over time to provide better code support related to data structures and algorithms. 

**Main Components**
1. Agent reflects upon past history of user, creating catered responses for common errors, successes, or other information. 
2. Agent Checks code -> Agent Generate hints or solutions for the user
3. Agent speaks back to user, gives a response in a conversation. 

**Tools Neccesary**
AgentCore Runtime 
Strands Agent SDK
Agentcore Memory Tool
Agentcore Code Interpreter
