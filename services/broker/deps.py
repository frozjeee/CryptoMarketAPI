from fastapi import Request


def get_broker(request: Request):
    if hasattr(request.app.state, "broker"):
        return request.app.state.broker
    return None
