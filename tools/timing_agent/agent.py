from google.adk.agents import Agent

from . import prompt

timing_agent = Agent(
        name="timing_agent",
        model="gemini-2.0-flash-001",
        description="O agente de timing. Processa a apresentação buscando deixar ela no timing.",
        instruction=prompt.TIMING_AGENT_PROMPT
)
