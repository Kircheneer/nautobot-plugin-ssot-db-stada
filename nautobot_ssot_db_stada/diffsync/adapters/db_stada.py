"""Nautobot SSoT DB Stada Adapter for DB StaDa SSoT plugin."""
import os

import requests
from diffsync import DiffSync
from nautobot.utilities.exceptions import AbortTransaction

from nautobot_ssot_db_stada.diffsync.models.base import BaseSite
from nautobot_ssot_db_stada.diffsync.models.db_stada import DBStadaSite, DBStadaRegion


class DBStadaAdapter(DiffSync):
    """DiffSync adapter for DB StaDa."""

    top_level = ["region", "site"]
    site = DBStadaSite
    region = DBStadaRegion

    def __init__(self, *args, job=None, sync=None, **kwargs):
        """Initialize DB StaDa.

        Args:
            job (object, optional): DB StaDa job. Defaults to None.
            sync (object, optional): DB StaDa DiffSync. Defaults to None.
        """
        super().__init__(*args, **kwargs)
        self.job = job
        self.sync = sync
        self.api_key = os.environ.get("DB_STADA_API_KEY")
        self.client_id = os.environ.get("DB_STADA_CLIENT_ID")
        self.url = "https://apis.deutschebahn.com/db-api-marketplace/apis/station-data/v2"

    @property
    def _auth_headers(self):
        """Format auth headers for API authentication."""
        return {
            "DB-Api-Key": self.api_key,
            "DB-Client-Id": self.client_id
        }

    def load(self):
        """Load data from DB StaDa into DiffSync models."""
        # Get data from DB API
        station_endpoint = self.url + "/stations?federalstate=bremen&federalstate=hamburg"
        result = requests.get(station_endpoint, headers=self._auth_headers)

        # Raise an error if the result is not a 2xx
        if not result.ok:
            self.job.log_failure(message=result.content)
            raise AbortTransaction()

        # Iterate over the retrieved stations and create diffsync objects from them
        for station in result.json()["result"]:
            # Handle regions
            region, created = self.get_or_instantiate(DBStadaRegion, ids={"name": station["federalState"]})
            self.add(region)
            if created:
                self.job.log_success(message=f"Successfully loaded site {region} from DB API.")

            # Handle sites
            try:
                longitude, latitude = station["ril100Identifiers"][0]["geographicCoordinates"]["coordinates"]
                longitude = round(longitude, 6)
                latitude = round(latitude, 6)
            except KeyError:
                longitude, latitude = None, None
            site = BaseSite(
                name=station["name"],
                region_name=station["federalState"],
                description=station["productLine"]["productLine"],
                shipping_address="\n".join(station["mailingAddress"].values()),
                latitude=latitude,
                longitude=longitude,
                contact_name=station["szentrale"]["name"],
                contact_phone=station["szentrale"]["publicPhoneNumber"]
            )
            self.add(site)
            self.job.log_success(message=f"Successfully loaded site {site} from DB API.")
