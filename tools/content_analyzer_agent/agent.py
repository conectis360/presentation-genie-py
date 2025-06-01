from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .tools.google_document_tool import create_document

name="ted_script_coordinator",
model="gemini-2.0-flash",
    
root_agent = Agent(
        name=name,
        model=model,
        description="O agente coordenador principal. Processa documentos e delega tarefas específicas para especialistas.",
        instruction=prompt.TED_TALK_ORCHESTRATOR_PROMPT,
        
        # O agente principal ainda precisa da ferramenta de processamento para sua tarefa core
        tools=[create_document.create_google_document],
        
        # MUDANÇA CHAVE: Liga os sub-agentes aqui!
        sub_agents=[content_analyzer_agent, storyteller_agent, timing_agent, visual_agent, personalizer_agent]
)