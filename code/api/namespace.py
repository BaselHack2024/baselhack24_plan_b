
from fastapi import status
from fastapi.routing import APIRouter

namespace = APIRouter()


@namespace.get("/test",
               description="test call",
               status_code=status.HTTP_200_OK
               )
def test_endpoint():
    return "works"