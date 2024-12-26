from fastapi import APIRouter, status
from api.orm.session import get_session
import uuid
from api.services.file import FileService
from fastapi.responses import FileResponse

router = APIRouter(prefix="/api/file", tags=["file"])


@router.get("/{resource_id}", status_code=status.HTTP_200_OK, summary="Get file")
def get_file(resource_id: uuid.UUID):
    with get_session() as session:
        file = FileService(session).get_resource_by_filters(id=resource_id)
    return FileResponse(file.path)
