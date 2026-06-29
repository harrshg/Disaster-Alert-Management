from typing import Any

import httpx
from fastapi import HTTPException, status


async def fetch_json(
    base_url: str,
    path: str = "",
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[str, dict[str, Any]]:
    url = f"{base_url.rstrip('/')}/{path.lstrip('/')}" if path else base_url.rstrip("/")

    try:
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return str(response.url), response.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail={
                "message": "Data source returned an error response.",
                "source_url": str(exc.request.url),
                "response": exc.response.text[:500],
            },
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "message": "Data source request failed.",
                "source_url": str(exc.request.url) if exc.request else url,
            },
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "message": "Data source returned invalid JSON.",
                "source_url": url,
            },
        ) from exc
