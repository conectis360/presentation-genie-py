from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .tools.google_document_tool import create_document

name="content_analyzer_agent",
model="gemini-2.0-flash",
    
content_analyzer_agent = Agent(
        name=name,
        model=model,
        description="O agente coordenador principal. Processa documentos e delega tarefas específicas para especialistas.",
        instruction=prompt.CONTENT_ANALYZER_AGENT_PROMPT,
        # O agente principal ainda precisa da ferramenta de processamento para sua tarefa core
        tools=[],
        # MUDANÇA CHAVE: Liga os sub-agentes aqui!
        sub_agents=[]
)