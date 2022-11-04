"""Test DB StaDa adapter."""

import json
import uuid
from unittest.mock import MagicMock

from django.contrib.contenttypes.models import ContentType
from nautobot.extras.models import Job, JobResult
from nautobot.utilities.testing import TransactionTestCase
from nautobot_ssot_db_stada.diffsync.adapters.db_stada import DBStadaAdapter
from nautobot_ssot_db_stada.jobs import DBStadaDataSource


def load_json(path):
    """Load a json file."""
    with open(path, encoding="utf-8") as file:
        return json.loads(file.read())


SITE_FIXTURE = []


class TestDBStadaAdapterTestCase(TransactionTestCase):
    """Test NautobotSSoTDBStadaAdapter class."""

    databases = ("default", "job_logs")

    def setUp(self):
        """Initialize test case."""
        self.db_stada_client = MagicMock()
        self.db_stada_client.get_sites.return_value = SITE_FIXTURE

        self.job = DBStadaDataSource()
        self.job.job_result = JobResult.objects.create(
            name=self.job.class_path, obj_type=ContentType.objects.get_for_model(Job), user=None, job_id=uuid.uuid4()
        )
        self.db_stada = DBStadaAdapter(job=self.job, sync=None, client=self.db_stada_client)

    def test_data_loading(self):
        """Test Nautobot SSoT DB Stada load() function."""
        # self.db_stada.load()
        # self.assertEqual(
        #     {site["name"] for site in SITE_FIXTURE},
        #     {site.get_unique_id() for site in self.db_stada.get_all("site")},
        # )
