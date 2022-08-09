# type: ignore

import json
from datetime import datetime
from uuid import uuid4

from handlers.hello.index import (
    HelloResponse,
    ResponseBody,
    handler,
)


class TestHelloHandler:
    test_context = {
        "accountId": "test",
        "apiId": "test",
        "stage": "test",
        "protocol": "test",
        "identity": {
            "sourceIp": "127.0.0.1",
        },
        "requestId": "test",
        "requestTime": "test",
        "requestTimeEpoch": "12345678910",
        "resourcePath": "test",
        "httpMethod": "GET",
        "path": "/test",
    }
    test_id = str(uuid4())
    test_timestamp = datetime.utcnow().isoformat()
    test_event = {
        "resource": "/testapi",
        "path": "/testing",
        "httpMethod": "GET",
        "headers": {"Test-X-Test": "Testing"},
        "multiValueHeaders": {"Testing-the-things": ["wow", "omg", "lol"]},
        "queryStringParameters": {"foo": "bar", "baz": "42"},
        "multiValueQueryStringParameters": {"wow": ["zer", "omg", "42"]},
        "requestContext": test_context,
        "isBase64Encoded": False,
        "body": json.dumps(
            {
                "message": 'This is a test!',
                "timestamp": test_timestamp,
                "event_id": test_id,
            }
        ),
    }

    def test_handler(self):
        actual_response = handler(event=self.test_event, context=self.test_context)
        assert actual_response == HelloResponse(
            is_base64_encoded=False,
            status_code=200,
            headers=None,
            multiValueHeaders=None,
            body=ResponseBody(
                message="And good day to you, sir or ma'am!",
                sent_at=self.test_timestamp,
                event_id=self.test_id,
            ).json(),
        )
