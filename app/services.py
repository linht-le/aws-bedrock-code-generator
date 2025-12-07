import json
import logging

import boto3

from app.config import get_settings
from app.models import Message

logger = logging.getLogger(__name__)


class AWSBedrockService:
    def __init__(self):
        settings = get_settings()
        self.client = self.create_bedrock_client(settings)
        self.model_id = settings.MODEL_ID

    def create_bedrock_client(self, settings):
        """Create a boto3 Bedrock client"""
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            logger.info("Using explicit AWS credentials")
            return boto3.client(
                "bedrock-runtime",
                region_name=settings.AWS_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
        else:
            logger.info("Using AWS default credentials (IAM/CLI)")
            return boto3.client("bedrock-runtime", region_name=settings.AWS_REGION)

    def chat(
        self, messages: list[Message], temperature: float = 1.0, max_tokens: int = 1000
    ) -> dict:
        """Send chat messages to AWS Bedrock and get response."""
        try:
            logger.info(f"Received {len(messages)} messages for code generation")

            # Separate system and conversation messages
            system_content = None
            conversation_messages = []

            for msg in messages:
                if msg.role == "system":
                    system_content = msg.content
                elif msg.role in ["user", "assistant"]:
                    conversation_messages.append(
                        {"role": msg.role, "content": [{"text": msg.content}]}
                    )

            # Use default system prompt if not provided
            if not system_content:
                system_content = self._get_system_prompt()

            # Build request body for Amazon Nova
            request_body = {
                "schemaVersion": "messages-v1",
                "messages": conversation_messages,
                "system": [{"text": system_content}],
                "inferenceConfig": {"temperature": temperature, "max_new_tokens": max_tokens},
            }

            # Call Bedrock API
            response = self.client.invoke_model(
                modelId=self.model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(request_body),
            )

            response_body = json.loads(response["body"].read())

            result = {
                "response": self._extract_response_content(response_body),
                "usage": self._extract_usage_info(response_body),
                "success": True,
            }

            logger.info(
                f"Chat completed, total tokens: {result['usage']['total_tokens'] if result['usage'] else 'N/A'}"
            )

            return result
        except Exception as e:
            logger.error(f"AWS Bedrock chat error: {e}")
            return {"error": str(e), "response": None, "usage": None, "success": False}

    def _extract_response_content(self, response_body: dict) -> str:
        """Extract the main response content from Bedrock response."""
        try:
            output = response_body.get("output", {})
            message = output.get("message", {})
            content = message.get("content", [])

            if content and len(content) > 0:
                return content[0].get("text", "No response from model.")
            return "No response from model."
        except Exception as e:
            logger.error(f"Error extracting response content: {e}")
            return "Error extracting response."

    def _extract_usage_info(self, response_body: dict) -> dict | None:
        """Extract token usage information from Bedrock response."""
        try:
            usage = response_body.get("usage")
            if usage:
                return {
                    "input_tokens": usage.get("inputTokens", 0),
                    "output_tokens": usage.get("outputTokens", 0),
                    "total_tokens": usage.get("totalTokens", 0),
                }
            return None
        except Exception as e:
            logger.error(f"Error extracting usage info: {str(e)}")
            return None

    def _get_system_prompt(self) -> str:
        """Get system prompt for code generation."""
        return """You are an expert polyglot programmer AI assistant.
Follow these rules STRICTLY:

1. LANGUAGE/FRAMEWORK DETECTION:
    - Infer programming language/framework from user's request
    - If ambiguous, ask ONE clarifying question
    - If still unclear, default to most popular choice with explanation

2. CODE GENERATION RULES:
    - Generate complete, runnable code
    - Include necessary imports/dependencies
    - Add helpful comments
    - Include error handling
    - Mention how to run/install

3. RESPONSE FORMAT:
    [LANGUAGE] Language Name
    [FRAMEWORK] Framework Name (if applicable)

    ```language
    // Complete code here
    ```
    [INSTALLATION]
    Installation steps here

    [USAGE]
    How to run/use the code

    [NOTES]
    Any important notes or alternatives
"""


aws_bedrock_service = AWSBedrockService()
