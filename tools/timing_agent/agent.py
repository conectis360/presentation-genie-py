from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .tools.google_document_tool import create_document

name="timing_agent",
model="gemini-2.0-flash",
    
root_agent = Agent(
        name=name,
        model=model,
        description="O agente de timing. Processa a apresentação buscando deixar ela no timing.",
        instruction=prompt.TIMING_AGENT_PROMPT,
        
        # O agente principal ainda precisa da ferramenta de processamento para sua tarefa core
        tools=[],
        
        # MUDANÇA CHAVE: Liga os sub-agentes aqui!
        sub_agents=[]
)