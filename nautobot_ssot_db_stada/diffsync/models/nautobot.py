"""Nautobot DiffSync models for DB StaDa SSoT."""
from nautobot.dcim.models import Site, Region
from nautobot.extras.models import Status

from nautobot_ssot_db_stada.diffsync.models.base import BaseSite, BaseRegion


class NautobotRegion(BaseRegion):
    """Nautobot implementation of DB StaDa Region model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create Site in Nautobot from NautobotSite object."""
        region = Region(
            name=ids["name"],
        )
        region.validated_save()
        return super().create(diffsync=diffsync, ids=ids, attrs=attrs)

    def update(self, attrs):
        """Update Site in Nautobot from NautobotSite object."""
        raise NotImplementedError()

    def delete(self):
        """Delete Site in Nautobot from NautobotSite object."""
        region = Region.objects.get(name=self.name)
        super().delete()
        region.delete()
        return self


class NautobotSite(BaseSite):
    """Nautobot implementation of DB StaDa Site model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        """Create Site in Nautobot from NautobotSite object."""
        site = Site(
            name=ids["name"],
            region=Region.objects.get(name=ids["region_name"]),
            description=attrs["description"],
            shipping_address=attrs["shipping_address"],
            latitude=attrs["latitude"],
            longitude=attrs["longitude"],
            contact_name=attrs["contact_name"],
            contact_phone=attrs["contact_phone"],
            status=Status.objects.get(slug="active")
        )
        site.validated_save()
        return super().create(diffsync=diffsync, ids=ids, attrs=attrs)

    def update(self, attrs):
        """Update Site in Nautobot from NautobotSite object."""
        site = Site.objects.get(name=self.name)
        for field, value in attrs.items():
            setattr(site, field, value)
        site.validated_save()
        return super().update(attrs)

    def delete(self):
        """Delete Site in Nautobot from NautobotSite object."""
        site = Site.objects.get(name=self.name)
        super().delete()
        site.delete()
        return self
