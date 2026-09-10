# app/models/base.py
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from bson import ObjectId
from typing import Optional, Any, Annotated
from datetime import datetime

def validate_object_id(v: Any) -> str:
    """Validator that accepts an ObjectId or a valid ObjectId string."""
    if isinstance(v, ObjectId):
        return str(v)
    if isinstance(v, str) and ObjectId.is_valid(v):
        return v
    raise ValueError("Invalid ObjectId")

# Pydantic v2 custom type for MongoDB ObjectId fields
PyObjectId = Annotated[str, BeforeValidator(validate_object_id)]

class MongoBaseModel(BaseModel):
    """Base model for MongoDB documents with common fields"""

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def to_mongo(self) -> dict:
        """Convert model to MongoDB document format"""
        data = self.model_dump(by_alias=True, exclude_none=True)
        if "_id" in data and data["_id"] is None:
            del data["_id"]
        data["updated_at"] = datetime.now()
        return data

    @classmethod
    def from_mongo(cls, data: dict):
        """Create model instance from MongoDB document"""
        if data is None:
            return None
        return cls(**data)