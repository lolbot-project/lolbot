from ruamel.yaml import YAML

class Config:
    def __init__(self, file):
        self.reader = YAML(typ='safe')
        file_ptr = open(file, 'r')
        self.config = self.reader.load(file_ptr)
        file_ptr.close()

    def get_config():
        return self.config