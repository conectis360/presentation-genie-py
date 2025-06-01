from google.adk.agents import Agent

from . import prompt


content_analyzer_agent = Agent(
        name="content_analyzer_agent",
        model="gemini-2.0-flash-001",
        description="O agente analizador de conteudo. Vai pegar o conteudo e analizar para trazer bons insights.",
        instruction=prompt.CONTENT_ANALYZER_AGENT_PROMPT
)
