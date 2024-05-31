from fastapi import Request


async def log_request(request: Request, call_next):
    body = await request.body()
    print(body.decode())
    response = await call_next(request)
    return response
