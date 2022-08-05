import json
from datetime import datetime
from typing import (
    NewType,
    Optional,
)
from uuid import UUID

from aws_lambda_powertools.utilities.parser import (
    envelopes,
    event_parser,
)
from aws_lambda_powertools.utilities.parser.models import APIGatewayEventRequestContext
from loguru import logger
from pydantic import (
    BaseModel,
    Field,
    validator,
)

EventMessage = NewType('EventMessage', str)
EventId = NewType('EventId', UUID)


class ResponseBody(BaseModel):
    message: str
    sent_at: datetime
    event_id: EventId


class HelloEvent(BaseModel):
    message: EventMessage
    timestamp: datetime
    event_id: EventId

    @validator('message')
    def message_not_too_long(cls, message):
        if len(message) > 32:
            raise ValueError('That message is too long!')
        return message


class HelloResponse(BaseModel):
    isBase64Encoded: bool = Field(default=False, alias="is_base64_encoded")
    statusCode: int = Field(default=200, alias="status_code", ge=100, lt=600)
    headers: Optional[dict[str, str]]
    multiValueHeaders: Optional[dict[str, list[str]]]
    body: str


@event_parser(model=HelloEvent, envelope=envelopes.apigw.ApiGatewayEnvelope)
def handler(
    event: HelloEvent,
    context: APIGatewayEventRequestContext,
) -> HelloResponse:
    logger.info(f"Found Event: {event.json()}")
    logger.info(f"{isinstance(event, HelloEvent) = }")
    logger.info(f"Got Context: {json.dumps(dict(context), default=str)}")

    response = HelloResponse(
        body=ResponseBody(
            message="And good day to you, sir or ma'am!", sent_at=event.timestamp, event_id=event.event_id
        ).json()
    )
    logger.info(f'Response: {response.json()}')
    return response
