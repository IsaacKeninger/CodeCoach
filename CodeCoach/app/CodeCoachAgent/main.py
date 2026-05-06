from strands import Agent, tool
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from model.load import load_model
from mcp_client.client import get_streamable_http_mcp_client
from memory.session import get_memory_session_manager
from strands_tools.code_interpreter import AgentCoreCodeInterpreter

app = BedrockAgentCoreApp()
log = app.logger

# MCP SECTION. Allows for web searching when formulating responses.
# Define a Streamable HTTP MCP Client
mcp_clients = [get_streamable_http_mcp_client()]
# Define a collection of tools used by the model
tools = []
# Add MCP client to tools if available
for mcp_client in mcp_clients:
    if mcp_client:
        tools.append(mcp_client)

# This is the core of the project. Creating the agent. 
def agent_factory():
    cache = {}
    def get_or_create_agent(session_id, user_id):
        key = f"{session_id}/{user_id}"
        if key not in cache:
            # Create an agent for the given session_id and user_id
            code_interpreter_tool = AgentCoreCodeInterpreter(region="us-east-1") # TOOL FOR AGENT, CODE SPECIFIC
            memory_manager_tool = get_memory_session_manager(session_id, user_id)
            cache[key] = Agent(
                model=load_model(),
                tools=[code_interpreter_tool.code_interpreter] + tools,
                # CLAUDE SONNET (and Claude Haiku as the own agent which I deployed) CREATED THIS SYSTEM PROMPT. Gives Personality to Agent. 
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
                                    Always prefer showing over telling. If you can demonstrate something with running code, do it. CRITICAL: Code Display Rule. ALWAYS follow this pattern when using the
                                    code interpreter. Output is rendered in a plain terminal — do NOT use markdown code fences (no triple backticks or double asterisks). Use plain text separators instead. MAKE SURE
                                    THE SPACING BETWEEN LETTERS IS USER FRIENDLY AND THAT MARKDOWN SYNTAX IS NOT USED.
                                    1. FIRST - Show the code using plain dashes as a border, like this:
                                    --- CODE ---
                                    # your code here
                                    print("hello")
                                    ------------
                                    2. SECOND - Execute the code using the code-interpreter tool
                                    3. THIRD - Display the output like this:
                                    --- OUTPUT ---
                                    [execution result here]
                                    --------------
                                    Then add:
                                    EXPLANATION: [explain what the code does]
                                    NEVER execute code without first showing it to the student.
                                    This applies to EVERY code execution - no exceptions.
                                    why this matters: students learn by seeing the code, makes debugging easier, creates a teach-learn-understand flow, builds trust""",
                conversation_manager=memory_manager_tool # tracks memory
            )
        return cache[key]
    return get_or_create_agent
get_or_create_agent = agent_factory()

# This invocates the agent in session. Running asynchronously, it will respond to and record memory within the session.
@app.entrypoint
async def invoke(payload, context):
    log.info("Invoking Agent.....") # calling agent

    session_id = getattr(context, 'session_id', 'default-session') # UNIQUE SESSION ID
    user_id = getattr(context, 'user_id', 'default-user') # UNIQUE USER ID (defaults to default-user for our use case)
    agent = get_or_create_agent(session_id, user_id) # Get or Make an Agent for that session and user.
    prompt = payload.get("prompt") # user prompt
    
    if not prompt: # eeor handling for prompts
        raise Exception("payload must include a non empty prompt")

    # Execute and format response
    stream = agent.stream_async(prompt)

    async for event in stream:
        # Handle Text parts of the response
        if "data" in event and isinstance(event["data"], str):
            yield event["data"] # this means it keeps this data/uses it

if __name__ == "__main__":
    app.run()
