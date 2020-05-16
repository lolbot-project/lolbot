from ruamel.yaml import YAML
from utils.errors import ConfigError


class Config:
    def __init__(self, file):
        self.reader = YAML(typ="safe")
        self.file = file  # for usage in loading/reloading
        self._load_config()

    def _load_config(self):
        with open(self.file, "r") as f:
            try:
                self.config = self.reader.load(f)
            except Exception as exc:
                raise ConfigError(exc)

    def reload_config(self):
        self._load_config()
        return self.config
