from google.adk.agents import Agent

from . import prompt

visual_agent = Agent(
        name="visual_agent",
        model="gemini-2.0-flash",
        description="O agente coordenador principal. Processa documentos e delega tarefas específicas para "
                    "especialistas.",
        instruction=prompt.VISUAL_AGENT_PROMPT
)
