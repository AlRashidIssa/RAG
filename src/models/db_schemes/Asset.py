from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime

class Asset(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    asset_project_id: ObjectId
    asset_type: str = Field(..., min_length=1)
    asset_name: str = Field(..., min_length=1)
    asset_size: int = Field(..., default=None)
    asset_config: dict = Field(ge=0, default=None)
    asset_pushed_at: datetime = Field(default=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True

    

        