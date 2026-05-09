from fastapi import APIRouter, HTTPException
from app.schemas import OrderRequest, OrderResponse
# from crew import run_order_crew
from app.crew import run_order_crew

router = APIRouter(prefix="/api", tags=["orders"])

conversation_context = ""
current_order_summary = ""

@router.post("/order", response_model=OrderResponse)
async def create_order(request: OrderRequest):
    global conversation_context, current_order_summary

    try:
        result = run_order_crew(
            user_message=request.message,
            conversation_context=conversation_context,
            current_order=current_order_summary
        )
    
        result_str = str(result)

        # Context update
        conversation_context += f"\nUser: {request.message}\nAgent: {result_str}\n"

        if any(word in result_str.lower() for word in ["placed", "successfully", "✅"]):
            conversation_context = ""
            current_order_summary = ""
            return OrderResponse(
                success=True,
                message="Order placed successfully!",
                data={"result": result_str}
            )
    
        else:
            if "Total Amount" in result_str or "Kul Rashi" in result_str:
                current_order_summary = result_str
            
        
            return OrderResponse(
                success=True,
                message="Order processed",
                data={"result": result_str}
            )
    
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/clear")
async def clear_conversation():
    global conversation_context, current_order_summary
    conversation_context = ""
    current_order_summary = ""
    return {"message": "Conversation cleared successfully"}