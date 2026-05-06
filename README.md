## Project Idea

A terminal based (at the moment) AWS-Based Agentic AI, CodeCoach recives DSA/Leetcode Style code responses from the user and provides memory integrated hints, responses, and solutions in a converstional manner to the user. Instead of just an LLM giving a response to code, CodeCoach's agent statefully tracks and acts over time to provide better code support related to data structures and algorithms.

---

## Main Components

1. Agent recieves an invocation from the user (prompt)
2. Agent autonomously draws upon relevant memory and beings to formualte a response.
   - 2a. If response is related to code (as it is specialized), agentcore code interpreter is used to generate, test, and review code.
3. Agent speaks back to user in a conversational manner, giving a response in a conversation/problem.

---

## Tools Neccesary

**AgentCore Runtime**
- "A containerized application that processes user inputs, maintains context, and executes actions using AI capabilities. When you create an agent, you define its behavior, capabilities, and the tools it can access" (Amazon Bedrock AgentCore Dev Guidem, *How it works*).

**Strands Agent SDK**
- Software Dev Kit that allows for combination of a model, tools, and a prompt. This simplifies the development and framwork of an agent, allowing for interactivity and flexibility in creating agents.

**Agentcore Memory**
- This capability allows for persistent memory across sessions in multiple modes. Semantic, User Pref, Episodic, and Summarization.

**Agentcore Code Interpreter**
- This tool allows the agent to test and run code. I utilize the tool to give efficent and tested solutions to DSA code.

**Identity & Access Managment**
- I use IAM to scope the permissions of my project and use agentcore.

---

## Model

Anthropic Haiku 4.5 - 5M TPM (Tokens Per Minute), 10 RPM (Requests Per Minute)

---

## Sources

- Amazon Bedrock AgentCore Dev Guide: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-how-it-works.html
- Memory: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-customer-scenario.html
- Strands SDK: https://aws.amazon.com/blogs/opensource/introducing-strands-agents-an-open-source-ai-agents-sdk/

---

## Challenges

**Model Access**
- AWS sets all new accounts to have 0 TPM or RPM for all models by default. In order to avoid this rate limit throttling, I sent a quota increase request to AWS Support & the issue was resolved by giving me fundamental access to all models available on AWS.

**IAM Permissions**
- In order to deploy the agent, I had to give my IAM user access to many services such as cloudwatch, s3, and agentcore itself. I solved this thorugh in-line policy and adding permission within the aws console.
