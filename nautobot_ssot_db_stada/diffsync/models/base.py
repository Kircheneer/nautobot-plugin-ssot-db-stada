"""DiffSyncModel subclasses for Nautobot-to-DB StaDa data sync."""
from typing import Optional, List
from diffsync import DiffSyncModel


class BaseSite(DiffSyncModel):
    """DiffSync model for DB StaDa sites."""

    _modelname = "site"
    _identifiers = ("name", "region_name")
    _attributes = (
        "description",
        "shipping_address",
        "latitude",
        "longitude",
        "contact_name",
        "contact_phone"
    )
    _children = {}

    name: str
    region_name: str
    description: Optional[str]
    shipping_address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    contact_name: Optional[str]
    contact_phone: Optional[str]


class BaseRegion(DiffSyncModel):
    """DiffSync model for DB StaDa regions."""

    _modelname = "region"
    _identifiers = ("name",)
    _attributes = ()

    name: str
