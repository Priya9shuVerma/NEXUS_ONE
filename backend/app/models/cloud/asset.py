from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from app.db.database import Base


class CloudAsset(Base):
    __tablename__ = "cloud_assets"

    id = Column(Integer, primary_key=True, index=True)

    cloud_account_id = Column(
        Integer,
        ForeignKey("cloud_accounts.id"),
        nullable=False,
        index=True,
    )

    provider = Column(
        String(50),
        nullable=False,
        index=True,
    )

    asset_type = Column(
        String(100),
        nullable=False,
        index=True,
    )

    asset_name = Column(
        String(200),
        nullable=False,
        index=True,
    )

    resource_id = Column(
        String(300),
        nullable=False,
        index=True,
    )

    region = Column(String(100), nullable=True)

    status = Column(
        String(50),
        default="active",
        nullable=False,
    )

    risk_level = Column(
        String(30),
        default="low",
        nullable=False,
    )

    metadata_json = Column(
        Text,
        nullable=True,
    )

    discovered_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
