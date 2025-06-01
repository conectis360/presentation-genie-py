from google.adk.agents import Agent

from . import prompt

storyteller_agent = Agent(
        name="storyteller_agent",
        model="gemini-2.0-flash-001",
        description="O agente que irá transformar a história em storytelling. Processa o texto e procura por "
                    "elementos que transformarão em story telling",
        instruction=prompt.STORYTELLER_AGENT_PROMPT
)
