"""Nautobot SSoT DB Stada DiffSync models for Nautobot SSoT DB Stada SSoT."""

from nautobot_ssot_db_stada.diffsync.models.base import BaseSite, BaseRegion


class DBStadaRegion(BaseRegion):
    """DB StaDa implementation of Region DiffSync model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        raise NotImplementedError()

    def update(self, attrs):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()


class DBStadaSite(BaseSite):
    """DB StaDa implementation of Site DiffSync model."""

    @classmethod
    def create(cls, diffsync, ids, attrs):
        raise NotImplementedError()

    def update(self, attrs):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()