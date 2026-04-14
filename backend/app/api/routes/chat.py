from fastapi import APIRouter, HTTPException
from engine.orchestrator.orchestrator import Graph
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()

graph = Graph()

session_db = {}

@router.post("/chat/graph", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        session_id = getattr(request, "session_id", "default_user")

        old_history = session_db.get(session_id, [])

        result = await graph.run(request.user_input)

        session_db[session_id] = result["messages"]

        last_msg = result["messages"][-1].content
        last_agent = result.get("active_agent", "unknown")

        print(result["messages"])

        return ChatResponse(
            agent_name=last_agent,
            response=last_msg
        )

    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}") 
        import traceback
        traceback.print_exc() 
        raise HTTPException(status_code=500, detail=f"Graph Error: {str(e)}")