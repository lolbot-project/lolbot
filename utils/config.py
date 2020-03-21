from ruamel.yaml import YAML
from utils.errors import ConfigError

class Config:
    def __init__(self, file):
        self.reader = YAML(typ='safe')
        self.file = file # for usage in loading/reloading
        self._load_config()

    def _load_config(self):
        try:
            file_ptr = open(self.file, 'r')
            config = self.reader.load(file_ptr)
            file_ptr.close()
            self.config = config
        except Exception as exc:
            raise ConfigError(exc)

    def get_config(self):
        return self.config

    def reload_config(self):
        self._load_config()
        return self.config