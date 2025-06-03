from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from .tools.content_analyzer_agent.agent import content_analyzer_agent
from .tools.storyteller_agent.agent import storyteller_agent
from .tools.timing_agent.agent import timing_agent
from .tools.visual_agent.agent import visual_agent
from .tools.personalizer_agent.agent import personalizer_agent
from .tools.google_document_tool.create_document import create_google_document

from . import prompt


root_agent = Agent(
        name="ted_script_coordinator",
        model="gemini-2.0-flash-001",
        description="O agente coordenador principal. Processa documentos e delega tarefas específicas para "
                    "especialistas.",
        instruction=prompt.TED_TALK_ORCHESTRATOR_PROMPT,
        tools=[
                AgentTool(agent=content_analyzer_agent),
                AgentTool(agent=storyteller_agent),
                AgentTool(agent=timing_agent),
                AgentTool(agent=visual_agent),
                AgentTool(agent=personalizer_agent),
                create_google_document
            ],
)
