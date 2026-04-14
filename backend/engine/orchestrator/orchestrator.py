import os
from langgraph.graph import StateGraph, END
from engine.agents.ceo.agent import CEOAgent
from engine.agents.orchestrator.agent import OrchestratorAgent 
from engine.agents.chro.agent import CHROAgent
from engine.agents.manager.agent import ManagerAgent
from langchain_core.messages import SystemMessage
from engine.state import AgentState
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool

DB_URI = "postgresql://user:password@db-persistence:5432/ai_memory?sslmode=disable"

connection_pool = AsyncConnectionPool(conninfo=DB_URI, max_size = 20, kwargs={"autocommit": True})

class Graph:
    def __init__(self):
        self.ceo = CEOAgent(config_path = "engine/agents/ceo/config.yaml")
        self.orchestrator = OrchestratorAgent(config_path="engine/agents/orchestrator/config.yaml")
        self.chro = CHROAgent(config_path="engine/agents/chro/config.yaml")
        self.manager = ManagerAgent(config_path = "engine/agents/manager/config.yaml")

        self.workflow = None

    async def _get_workflow(self):
        if self.workflow:
            return self.workflow
        
        builder = StateGraph(AgentState)
        builder.add_node("orchestrator", self.orchestrator.to_node())
        builder.add_node("CEO", self.ceo.to_node())
        builder.add_node("CHRO", self.chro.to_node())
        builder.add_node("Manager", self.manager.to_node())

        builder.set_entry_point("orchestrator")
        builder.add_conditional_edges(
            "orchestrator",
            self.route_fn,
            {"CEO": "CEO", "CHRO": "CHRO", "Manager": "Manager", END: END}
        )
        builder.add_edge("CEO", END)
        builder.add_edge("CHRO", END)
        builder.add_edge("Manager", END)

        checkpointer = AsyncPostgresSaver(connection_pool)

        await checkpointer.setup()
        
        self.workflow = builder.compile(checkpointer=checkpointer)
        return self.workflow

    def route_fn(self, state: AgentState):
        last_msg = state["messages"][-1]
        
        # 1. Thử lấy tool_calls theo mọi cách có thể
        tool_calls = []
        
        # Cách A: Thuộc tính chuẩn
        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
            tool_calls = last_msg.tool_calls
        # Cách B: Trong additional_kwargs (Dạng dict hoặc object)
        elif hasattr(last_msg, "additional_kwargs"):
            tool_calls = last_msg.additional_kwargs.get("tool_calls", [])

        print(f"[DEBUG ROUTE] Raw tool_calls detected: {tool_calls}")

        if tool_calls and len(tool_calls) > 0:
            call = tool_calls[0]
            tool_name = None
            
            # 2. Bóc tách tool_name dựa trên cấu trúc Log của bạn
            # Cấu trúc log: {'function': {'name': 'call_ceo', ...}}
            if isinstance(call, dict):
                if "function" in call:
                    tool_name = call["function"].get("name")
                else:
                    tool_name = call.get("name")
            else:
                # Trường hợp là ToolCall object của LangChain
                tool_name = getattr(call, "name", None)

            print(f"[DEBUG ROUTE] Extracted tool_name: {tool_name}")

            mapping = {
                "call_ceo": "CEO",
                "call_chro": "CHRO",
                "call_manager": "Manager"
            }

            target = mapping.get(tool_name)
            if target:
                print(f"[DEBUG ROUTE] Success! Routing to Node: {target}")
                return target
                
        print("[DEBUG ROUTE] Still no tool calls found. Ending Graph.")
        return END

    
    async def run(self, user_input: str, thread_id: str = "default_user"):

        workflow = await self._get_workflow()

        initial_messages = [HumanMessage(content=user_input)]

        config = {
            "configurable": {"thread_id": thread_id},
            "recursion_limit": 10
        }

        initial_state = {
            "messages": initial_messages,
            "next_node": "",
            "active_agent": ""
        }

        print(f"\n--- STARTING GRAPH EXECUTION (Thread: {thread_id})---")

        final_state = await self.workflow.ainvoke(initial_state, config = config)

        if final_state["messages"]:
            last_msg = final_state["messages"][-1].content
            print(f"[FINAL AGENT]: {final_state.get('active_agent')}")
            chat_history_str = " | ".join([m.content for m in final_state["messages"] if m.content])
            print(f"[DEBUG] chat history: {chat_history_str}")
            print(f"[FINAL OUTPUT]: {last_msg}")

        print(f"Full Message Object: {final_state['messages'][-1]}")
        
        return final_state        