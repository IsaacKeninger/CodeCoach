from strands import Agent, tool
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from model.load import load_model
from mcp_client.client import get_streamable_http_mcp_client
from memory.session import get_memory_session_manager
from strands_tools.code_interpreter import AgentCoreCodeInterpreter

app = BedrockAgentCoreApp()
log = app.logger

# Define a Streamable HTTP MCP Client
mcp_clients = [get_streamable_http_mcp_client()]

# Define a collection of tools used by the model
tools = []

# Define a simple function tool
@tool
def add_numbers(a: int, b: int) -> int:
    """Return the sum of two numbers"""
    return a+b
tools.append(add_numbers)

# Add MCP client to tools if available
for mcp_client in mcp_clients:
    if mcp_client:
        tools.append(mcp_client)


def agent_factory():
    cache = {}
    def get_or_create_agent(session_id, user_id):
        key = f"{session_id}/{user_id}"
        if key not in cache:
            # Create an agent for the given session_id and user_id
            code_interpreter_tool = AgentCoreCodeInterpreter(region="us-east-1") # TOOL FOR AGENT, CODE SPECIFIC
            cache[key] = Agent(
                model=load_model(),
                tools=[code_interpreter_tool.code_interpreter] + tools,
                # CLAUDE CREATED THIS SYSTEM PROMPT
                system_prompt="""You are CodeCoach, an expert programming tutor. Your goal is to teach coding concepts clearly and interactively.
                                    When explaining any concept, always use the code interpreter to run a live example and show the actual output — never just describe what code does without running it.
                                    When a person shares code:
                                    - Run it first to see what it actually does
                                    - Identify bugs or improvements
                                    - Explain what went wrong and why, not just how to fix it
                                    Teaching style:
                                    - Ask guiding questions rather than giving answers directly when the student is close to a solution
                                    - Break complex topics into small, digestible steps
                                    - Celebrate progress and correct mistakes without discouragement
                                    - Adapt your explanation depth to the student's apparent skill level
                                    Always prefer showing over telling. If you can demonstrate something with running code, do it.""",
            )
        return cache[key]
    return get_or_create_agent
get_or_create_agent = agent_factory()


@app.entrypoint
async def invoke(payload, context):
    log.info("Invoking Agent.....")

    session_id = getattr(context, 'session_id', 'default-session')
    user_id = getattr(context, 'user_id', 'default-user')
    agent = get_or_create_agent(session_id, user_id)

    # Execute and format response
    stream = agent.stream_async(payload.get("prompt"))

    async for event in stream:
        # Handle Text parts of the response
        if "data" in event and isinstance(event["data"], str):
            yield event["data"]


if __name__ == "__main__":
    app.run()
