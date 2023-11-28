import traceback
from functools import wraps

from fastapi import HTTPException

__all__ = [
    "exceptions_handler",
]


def exceptions_handler(func):
    """Catch all uncaught exceptions."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException:
            print(traceback.format_exc())
            raise
        except Exception as exc:
            print(traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(exc))

    return wrapper
