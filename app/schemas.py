from pydantic import BaseModel
from typing import Optional, Dict, Any

class OrderRequest(BaseModel):
    message: str

class OrderResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    order_status: Optional[str] = None

