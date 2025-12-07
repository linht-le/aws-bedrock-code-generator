import logging

from fastapi import APIRouter, HTTPException

from app.models import ChatRequest, ChatResponse
from app.services import aws_bedrock_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle chat requests for code generation."""
    try:
        result = aws_bedrock_service.chat(messages=request.messages)

        return ChatResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise HTTPException(status_code=500, detail="Server error") from e
