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





**Sources**
Amazon Bedrock AgentCore Dev Guide: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-how-it-works.html
