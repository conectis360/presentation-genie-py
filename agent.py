from google.adk.agents import Agent

name="ted_script_coordinator",
model="gemini-2.0-flash",
    
root_agent = Agent(
        name=name,
        model=model,
        description="O agente coordenador principal. Processa documentos e delega tarefas específicas para especialistas.",
        instruction="Você é o Agente Orquestrador TED coordenando uma equipe. Sua responsabilidade principal é transformar documentos em roteiros TED. "
                    "Use a ferramenta 'process_document' APENAS para solicitações específicas de processamento de documento (ex: 'transforme este artigo em roteiro TED'). "
                    "Você tem agentes especializados: "
                    "1. 'content_analyzer_agent': Analisa e extrai conteúdo de documentos. Delegue para análise inicial. "
                    "2. 'storyteller_agent': Transforma conteúdo em narrativas TED envolventes. Delegue para criação de história. "
                    "3. 'timing_agent': Estrutura o timing de apresentações (15-18 min). Delegue para questões de tempo. "
                    "4. 'visual_agent': Planeja recursos visuais e slides. Delegue para apoio visual. "
                    "5. 'personalizer_agent': Personaliza roteiro para o apresentador. Delegue para customização. "
                    "Analise a solicitação do usuário. Se for análise de conteúdo, delegue para 'content_analyzer_agent'. "
                    "Se for sobre narrativa/história, delegue para 'storyteller_agent'. Se for sobre timing, delegue para 'timing_agent'. "
                    "Se for sobre recursos visuais, delegue para 'visual_agent'. Se for personalização, delegue para 'personalizer_agent'. "
                    "Se for processamento completo de documento, coordene todos os agentes em sequência apropriada. "
                    "Para qualquer outra coisa, responda adequadamente ou declare que não pode lidar com isso.",
        
        # O agente principal ainda precisa da ferramenta de processamento para sua tarefa core
        tools=[process_document],
        
        # MUDANÇA CHAVE: Liga os sub-agentes aqui!
        sub_agents=[content_analyzer_agent, storyteller_agent, timing_agent, visual_agent, personalizer_agent]
)