"""Nautobot Adapter for DB StaDa SSoT plugin."""

from diffsync import DiffSync
from nautobot.dcim.models import Site, Region

from nautobot_ssot_db_stada.diffsync.models.base import BaseSite, BaseRegion
from nautobot_ssot_db_stada.diffsync.models.nautobot import NautobotSite, NautobotRegion


class NautobotAdapter(DiffSync):
    """DiffSync adapter for Nautobot."""

    top_level = ["region", "site"]
    site = NautobotSite
    region = NautobotRegion

    def __init__(self, *args, job=None, sync=None, **kwargs):
        """Initialize Nautobot.

        Args:
            job (object, optional): Nautobot job. Defaults to None.
            sync (object, optional): Nautobot DiffSync. Defaults to None.
        """
        super().__init__(*args, **kwargs)
        self.job = job
        self.sync = sync

    def load(self):
        """Load data from Nautobot into DiffSync models."""
        for region in Region.objects.all():
            diffsync_region = BaseRegion(
                name=region.name
            )
            self.add(diffsync_region)
            self.job.log_success(message=f"Successfully loaded region {region} from Nautobot.")
            for site in Site.objects.filter(region=region):
                diffsync_site = BaseSite(
                    name=site.name,
                    region_name=diffsync_region.name,
                    description=site.description,
                    shipping_address=site.shipping_address,
                    latitude=site.latitude,
                    longitude=site.longitude,
                    contact_name=site.contact_name,
                    contact_phone=site.contact_phone
                )
                self.add(diffsync_site)
                self.job.log_success(message=f"Successfully loaded site {site} from Nautobot.")
