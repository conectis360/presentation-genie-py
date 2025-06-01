from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt

name="personalizer_agent",
model="gemini-2.0-flash",
    
root_agent = Agent(
        name=name,
        model=model,
        description="O agente de personalização seu papel é refinar e adaptar um roteiro",
        instruction=prompt.PERSONALIZER_AGENT_PROMPT,
        tools=[],
        sub_agents=[]
)