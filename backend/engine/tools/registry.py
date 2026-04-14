from langchain_core.tools import tool
from engine.agents.ceo.agent import CEOAgent
from engine.agents.chro.agent import CHROAgent
from engine.agents.manager.agent import ManagerAgent

ceo_agent = CEOAgent(config_path = "engine/agents/ceo/config.yaml")
chro_agent = CHROAgent(config_path = "engine/agents/chro/config.yaml")
manager_agent = ManagerAgent(config_path = "engine/agents/manager/config.yaml")

@tool
def call_ceo(user_input: str):
    """
    Directly consult the CEO Agent for high-level business concerns. 
    Use this tool when the user's input involves corporate strategy, business models, 
    market trend analysis, investment/funding (seed, series A, etc.), 
    brand protection, or competitive positioning. 
    Ideal for strategic decision-making and challenging business hypotheses.
    """
    return ceo_agent.respond(user_input)

@tool
def call_chro(user_input: str):
    """
    Directly consult the CHRO (Chief Human Resources Officer) Agent for people-related matters. 
    Use this tool when the user asks about recruitment strategies, hiring plans, 
    organizational culture, employee retention, talent management, 
    team structures, or internal conflict resolution. 
    Ideal for building and managing a high-performing organization.
    """
    return chro_agent.respond(user_input)

@tool
def call_manager(user_input: str):
    """
    Directly consult the Regional Manager Agent for operational execution and feasibility. 
    Use this tool when the user's input involves project timelines, resource allocation, 
    on-the-ground implementation, regional constraints, or day-to-day management. 
    Ideal for turning high-level strategies into actionable plans and assessing 
    operational risks.
    """
    return manager_agent.respond(user_input)

BUSINESS_TOOLS = [call_ceo, call_chro, call_manager]