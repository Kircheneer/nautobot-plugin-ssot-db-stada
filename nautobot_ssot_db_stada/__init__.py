"""Plugin declaration for nautobot_ssot_db_stada."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)

from nautobot.extras.plugins import PluginConfig


class NautobotSSoTDBStadaConfig(PluginConfig):
    """Plugin configuration for the nautobot_ssot_db_stada plugin."""

    name = "nautobot_ssot_db_stada"
    verbose_name = "Nautobot SSoT DB Stada"
    version = __version__
    author = "Leo Kirchner"
    description = "Synchronize DB station data into Nautobot.."
    base_url = "ssot-db-stada"
    required_settings = []
    min_version = "1.2.0"
    max_version = "1.9999"
    default_settings = {}
    caching_config = {}


config = NautobotSSoTDBStadaConfig  # pylint:disable=invalid-name
