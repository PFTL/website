import yaml

configuration = {
    'param1': 10,
    'param2': 5
}

class Experiment:
    def __init__(self, config):
        self.configuration = config

    def check_config(self):
        if not {'param1', 'param2'} <= set(self.configuration.keys()):
            raise Exception('The configuration does not include the mandatory fields')
        print('Config looks OK')

    def check_config_range(self):
        if self.configuration['param1'] > 10:
            raise Exception('param1 cannot be larger than 10')
        if self.configuration['param2'] > 5:
            raise Exception('param2 cannot be larger than 5')
        print('Config ranges are OK')

exp = Experiment(configuration)
exp.check_config()
exp.check_config_range()


class Config:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self._config = yaml.load(f.read(), Loader=yaml.FullLoader)

    def keys(self):
        return self._config.keys()

    def __getitem__(self, item):
        return self._config[item]

c = Config('config.yml')
exp2 = Experiment(c)
exp2.check_config()
exp2.check_config_range()