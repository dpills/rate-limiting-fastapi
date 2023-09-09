import hashlib
from datetime import datetime, timedelta
from typing import Annotated, Any, Callable, TypeVar

import uvicorn
from fastapi import FastAPI, Header, Request, Response
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis.asyncio import Redis

F = TypeVar("F", bound=Callable[..., Any])


class Settings(BaseSettings):
    redis_password: str
    redis_host: str = "127.0.0.1"
    redis_port: int = 6379
    user_rate_limit_per_minute: int = 3
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

redis_client = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=0,
    decode_responses=True,
    password=settings.redis_password,
)
app = FastAPI(
    title="FastAPI Rate Limiting",
    description="Rate limiting users using Redis middleware",
    docs_url="/",
)


async def rate_limit_user(user: str, rate_limit: int) -> JSONResponse | None:
    """
    Apply rate limiting per user, per minute
    """
    # Increment our most recent redis key
    username_hash = hashlib.sha256(bytes(user, "utf-8")).hexdigest()
    now = datetime.utcnow()
    current_minute = now.strftime("%Y-%m-%dT%H:%M")

    redis_key = f"rate_limit_{username_hash}_{current_minute}"
    current_count = await redis_client.incr(redis_key)

    # If we just created a new key (count is 1) set an expiration
    if current_count == 1:
        await redis_client.expireat(name=redis_key, when=now + timedelta(minutes=1))

    # Check rate limit
    if current_count > rate_limit:
        return JSONResponse(
            status_code=429,
            content={"detail": "User Rate Limit Exceeded"},
            headers={
                "Retry-After": f"{60 - now.second}",
                "X-Rate-Limit": f"{rate_limit}",
            },
        )

    return None


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next: F) -> Response:
    """
    Rate limit requests per user
    """
    user = request.headers.get("x-user")
    if user:
        rate_limit_exceeded_response = await rate_limit_user(
            user=user, rate_limit=settings.user_rate_limit_per_minute
        )
        if rate_limit_exceeded_response:
            return rate_limit_exceeded_response

    return await call_next(request)


@app.get("/user", response_model=str | None)
def get_user(x_user: Annotated[str | None, Header()] = None):
    """
    **NOTE**: The `X-User` header should be passed by a reverse proxy,
    we are manually adding it to this endpoint so you can test
    this example locally
    """
    return x_user


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
