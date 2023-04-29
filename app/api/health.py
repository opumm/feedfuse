from fastapi import APIRouter, status

router = APIRouter()


@router.get(
    path="/health",
    name="health_check",
    summary="Health check",
    status_code=status.HTTP_200_OK,
)
async def health_check() -> dict:
    """
    Endpoint for health checks.
    """
    return {"status": "ok"}
