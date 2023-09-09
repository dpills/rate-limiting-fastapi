# FastAPI Rate Limiting

This project shows a basic example of how to implement a rate limiter in FastAPI with Redis. Run this app with Docker Compose to test it out locally.

> Note: a `.env` file with the same keys as the `.env-example` file is required for this to work correctly.

```bash
$ docker-compose up

rate-limiting-fastapi-redis-1  | 1:C 09 Sep 2023 20:08:23.209 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
rate-limiting-fastapi-redis-1  | 1:C 09 Sep 2023 20:08:23.209 * Redis version=7.2.1, bits=64, commit=00000000, modified=0, pid=1, just started
rate-limiting-fastapi-redis-1  | 1:C 09 Sep 2023 20:08:23.209 * Configuration loaded
rate-limiting-fastapi-redis-1  | 1:M 09 Sep 2023 20:08:23.209 * monotonic clock: POSIX clock_gettime
rate-limiting-fastapi-redis-1  | 1:M 09 Sep 2023 20:08:23.209 * Running mode=standalone, port=6379.
rate-limiting-fastapi-redis-1  | 1:M 09 Sep 2023 20:08:23.210 * Server initialized
rate-limiting-fastapi-redis-1  | 1:M 09 Sep 2023 20:08:23.210 * Ready to accept connections tcp

rate-limiting-fastapi-api-1    | INFO:     Started server process [1]
rate-limiting-fastapi-api-1    | INFO:     Waiting for application startup.
rate-limiting-fastapi-api-1    | INFO:     Application startup complete.
rate-limiting-fastapi-api-1    | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
rate-limiting-fastapi-api-1    | INFO:     172.21.0.1:39136 - "GET / HTTP/1.1" 200 OK
rate-limiting-fastapi-api-1    | INFO:     172.21.0.1:39136 - "GET /openapi.json HTTP/1.1" 200 OK
rate-limiting-fastapi-api-1    | INFO:     172.21.0.1:58024 - "GET /user HTTP/1.1" 200 OK
```
