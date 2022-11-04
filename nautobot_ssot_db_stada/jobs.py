"""Jobs for DB StaDa SSoT integration."""

from diffsync import DiffSyncFlags
from django.urls import reverse
from nautobot.extras.jobs import BooleanVar, Job
from nautobot_ssot.jobs.base import DataSource, DataMapping
from nautobot_ssot_db_stada.diffsync.adapters import db_stada, nautobot


name = "DB StaDa SSoT"  # pylint: disable=invalid-name


class DBStadaDataSource(DataSource, Job):
    """DB StaDa SSoT Data Source."""

    debug = BooleanVar(description="Enable for more verbose debug logging", default=False)

    def __init__(self):
        """Initialize DB StaDa Data Source."""
        super().__init__()
        self.diffsync_flags = DiffSyncFlags.NONE

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta data for DB StaDa."""

        name = "DB StaDa to Nautobot"
        data_source = "DB StaDa"
        data_target = "Nautobot"
        description = "Sync information from DB StaDa to Nautobot"

    @classmethod
    def config_information(cls):
        """Dictionary describing the configuration of this DataSource."""
        return {}

    @classmethod
    def data_mappings(cls):
        """List describing the data mappings involved in this DataSource."""
        return (
            DataMapping("Station (remote)", None, "Site (local)", reverse("dcim:site_list")),
            DataMapping("Federal State (remote)", None, "Region (local)", reverse("dcim:region_list"))
        )

    def load_source_adapter(self):
        """Load data from DB StaDa into DiffSync models."""
        self.source_adapter = db_stada.DBStadaAdapter(job=self, sync=self.sync)
        self.source_adapter.load()

    def load_target_adapter(self):
        """Load data from Nautobot into DiffSync models."""
        self.target_adapter = nautobot.NautobotAdapter(job=self, sync=self.sync)
        self.target_adapter.load()

    def execute_sync(self):
        """Method to synchronize the difference from `self.diff`, from SOURCE to TARGET adapter.

        This is a generic implementation that you could overwrite completely in your custom logic.
        """
        if self.source_adapter is not None and self.target_adapter is not None:
            self.source_adapter.sync_to(self.target_adapter, flags=self.diffsync_flags)
        else:
            self.log_warning(message="Not both adapters were properly initialized prior to synchronization.")


jobs = [DBStadaDataSource]
