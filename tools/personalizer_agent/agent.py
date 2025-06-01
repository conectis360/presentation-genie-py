from google.adk.agents import Agent

from . import prompt

personalizer_agent = Agent(
        name="personalizer_agent",
        model="gemini-2.0-flash-001",
        description="O agente de personalização seu papel é refinar e adaptar um roteiro",
        instruction=prompt.PERSONALIZER_AGENT_PROMPT
)
