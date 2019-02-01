class PluginBase:
    subclasses = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)


class MyPlugin(PluginBase):
    pass


print(PluginBase.subclasses)