from sqlalchemy.orm import Session

from app.models.cloud.account import CloudAccount
from app.models.cloud.asset import CloudAsset


def create_cloud_account(
    db: Session,
    name: str,
    provider: str,
    account_identifier: str,
    region: str | None = None,
    description: str | None = None,
):
    account = CloudAccount(
        name=name,
        provider=provider.lower(),
        account_identifier=account_identifier,
        region=region,
        description=description,
    )

    db.add(account)
    db.commit()
    db.refresh(account)

    return account


def get_cloud_accounts(db: Session):
    return (
        db.query(CloudAccount)
        .filter(CloudAccount.is_active.is_(True))
        .order_by(CloudAccount.id.desc())
        .all()
    )


def get_cloud_account(
    db: Session,
    account_id: int,
):
    return (
        db.query(CloudAccount)
        .filter(CloudAccount.id == account_id)
        .first()
    )


def create_cloud_asset(
    db: Session,
    cloud_account_id: int,
    provider: str,
    asset_type: str,
    asset_name: str,
    resource_id: str,
    region: str | None = None,
    status: str = "active",
    risk_level: str = "low",
    metadata_json: str | None = None,
):
    asset = CloudAsset(
        cloud_account_id=cloud_account_id,
        provider=provider.lower(),
        asset_type=asset_type,
        asset_name=asset_name,
        resource_id=resource_id,
        region=region,
        status=status,
        risk_level=risk_level,
        metadata_json=metadata_json,
    )

    db.add(asset)
    db.commit()
    db.refresh(asset)

    return asset


def get_cloud_assets(db: Session):
    return (
        db.query(CloudAsset)
        .order_by(CloudAsset.id.desc())
        .all()
    )
