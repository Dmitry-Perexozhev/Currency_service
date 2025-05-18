from fastapi import Request, Response

from service.storage.config_storage import config_storage


async def log_requests(request: Request, call_next):
    if config_storage.get_debug():
        body = await request.body()
        print(f"\n[DEBUG] Request: {request.method} {request.url}")
        print(f"Headers: {dict(request.headers)}")
        print(f"Body: {body.decode() if body else 'No body'}\n")

    response: Response = await call_next(request)

    if config_storage.get_debug():
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        async def fake_body_iterator():
            yield response_body

        response.body_iterator = fake_body_iterator()
        print(f"[DEBUG] Response status: {response.status_code}")
        print(f"Body: {response_body.decode()}\n")

    return response