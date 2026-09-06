from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CloudAccountCreate(BaseModel):
    name: str
    provider: str
    account_identifier: str
    region: Optional[str] = None
    description: Optional[str] = None


class CloudAccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    provider: str
    account_identifier: str
    region: Optional[str]
    status: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CloudAssetCreate(BaseModel):
    cloud_account_id: int
    provider: str
    asset_type: str
    asset_name: str
    resource_id: str
    region: Optional[str] = None
    status: str = "active"
    risk_level: str = "low"
    metadata_json: Optional[str] = None


class CloudAssetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cloud_account_id: int
    provider: str
    asset_type: str
    asset_name: str
    resource_id: str
    region: Optional[str]
    status: str
    risk_level: str
    metadata_json: Optional[str]
    discovered_at: datetime
