import yaml

class Config:
    _instance = None

    def __new__(cls, file_path=None):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.config = {}  # Initialize config attribute
            if file_path:
                cls._instance.load_config(file_path)
        return cls._instance

    def load_config(self, file_path):
        import pdb; pdb.set_trace()

        with open(file_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def get_config(self):
        return self.config