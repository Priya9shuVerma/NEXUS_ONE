from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.cloud.account import CloudAccount
from app.models.cloud.asset import CloudAsset
from app.models.user import User
from app.schemas.cloud import (
    CloudAccountCreate,
    CloudAccountResponse,
    CloudAssetCreate,
    CloudAssetResponse,
)
from app.services.cloud.cloud_service import (
    create_cloud_account,
    create_cloud_asset,
    get_cloud_accounts,
    get_cloud_assets,
)


router = APIRouter(
    prefix="/cloud",
    tags=["Cloud Security"],
)


@router.get("/")
async def cloud_home(
    current_user: User = Depends(get_current_user),
):
    return {
        "success": True,
        "module": "Cloud Security",
        "message": "NEXUS ONE Cloud API is working",
    }


@router.post(
    "/accounts",
    response_model=CloudAccountResponse,
)
async def create_account(
    account_data: CloudAccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_cloud_account(
        db=db,
        name=account_data.name,
        provider=account_data.provider,
        account_identifier=account_data.account_identifier,
        region=account_data.region,
        description=account_data.description,
    )


@router.get(
    "/accounts",
    response_model=list[CloudAccountResponse],
)
async def list_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_cloud_accounts(db)


@router.get(
    "/accounts/{account_id}",
    response_model=CloudAccountResponse,
)
async def get_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = (
        db.query(CloudAccount)
        .filter(CloudAccount.id == account_id)
        .first()
    )

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Cloud account not found",
        )

    return account


@router.delete("/accounts/{account_id}")
async def deactivate_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = (
        db.query(CloudAccount)
        .filter(CloudAccount.id == account_id)
        .first()
    )

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Cloud account not found",
        )

    account.is_active = False
    account.status = "inactive"

    db.commit()

    return {
        "success": True,
        "message": "Cloud account deactivated successfully",
    }


@router.post(
    "/assets",
    response_model=CloudAssetResponse,
)
async def create_asset(
    asset_data: CloudAssetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = (
        db.query(CloudAccount)
        .filter(
            CloudAccount.id == asset_data.cloud_account_id,
            CloudAccount.is_active.is_(True),
        )
        .first()
    )

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Active cloud account not found",
        )

    return create_cloud_asset(
        db=db,
        cloud_account_id=asset_data.cloud_account_id,
        provider=asset_data.provider,
        asset_type=asset_data.asset_type,
        asset_name=asset_data.asset_name,
        resource_id=asset_data.resource_id,
        region=asset_data.region,
        status=asset_data.status,
        risk_level=asset_data.risk_level,
        metadata_json=asset_data.metadata_json,
    )


@router.get(
    "/assets",
    response_model=list[CloudAssetResponse],
)
async def list_assets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_cloud_assets(db)


@router.get(
    "/assets/{asset_id}",
    response_model=CloudAssetResponse,
)
async def get_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    asset = (
        db.query(CloudAsset)
        .filter(CloudAsset.id == asset_id)
        .first()
    )

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Cloud asset not found",
        )

    return asset
