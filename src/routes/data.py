from fastapi import FastAPI, APIRouter, Depends, UploadFile, File
from helpers.config import get_settings, Settings
from conntrollers import DataController

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str, 
    file: UploadFile = File(...),  # Ensure File() is being used here
    app_settings: Settings = Depends(get_settings)
):
    is_valid, result_signal = DataController().validate_uploaded_file(file)
    return {"project_id": project_id, 
            "is_valid": is_valid, 
            "filename": file.filename,
            "signle": result_signal}