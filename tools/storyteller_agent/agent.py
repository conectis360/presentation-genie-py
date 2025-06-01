from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .tools.google_document_tool import create_document

name="storyteller_agent",
model="gemini-2.0-flash",
    
storyteller_agent = Agent(
        name=name,
        model=model,
        description="O agente que irá transformar a história em storytelling. Processa o texto e procura por elementos que transformarão em story telling",
        instruction=prompt.STORYTELLER_AGENT_PROMPT,
        # O agente principal ainda precisa da ferramenta de processamento para sua tarefa core
        tools=[],
        # MUDANÇA CHAVE: Liga os sub-agentes aqui!
        sub_agents=[]
)