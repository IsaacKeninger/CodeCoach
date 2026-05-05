**Project Idea**
An agentic AI tool, CodeCoach recives DSA/Leetcode Style code responses from the user and provides memory integrated
hints, responses, and solutions in a converstional manner to the user. Instead of just an LLM giving a response to code, 
CodeCoach's agent statefully tracks and acts over time to provide better code support related to data structures and algorithms. 

**Main Components**
1. Agent reflects upon past history of user, creating catered responses for common errors, successes, or other information. 
2. Agent Checks code -> Agent Generate hints or solutions for the user
3. Agent speaks back to user, gives a response in a conversation. 

**Tools Neccesary**
AgentCore Runtime 
- "A containerized application that processes user inputs, maintains context, and executes actions using AI capabilities. When you create an agent, you define its behavior, capabilities, and the tools it can access" (Amazon Bedrock AgentCore Dev Guidem, *How it works*).
Strands Agent SDK
Agentcore Memory Tool
Agentcore Code Interpreter
Identity & Access Managment

**Model**
Anthropic Haiku 4.5 - 5M TPM (Tokens Per Minute), 10 RPM (Requests Per Minute)

**Sources**
Amazon Bedrock AgentCore Dev Guide: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-how-it-works.html
Memory: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-customer-scenario.html
Strands SDK: https://aws.amazon.com/blogs/opensource/introducing-strands-agents-an-open-source-ai-agents-sdk/

**Challenges**
Model Access
- AWS sets all new accounts to have 0 TPM or RPM for all models by default. In order to avoid this rate limit throttling, I sent a quota increase request to AWS Support & 
    the issue was resolved by giving me fundamental access to all models available on AWS. 
IAM Permissions
-
Memory Managment
-