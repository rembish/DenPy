class Singleton(type):
    def __init__(self, name, bases, dict):
        super(Singleton, self).__init__(name, bases, dict)
        self.instance = None

    def __call__(self, *args, **kwargs):
        if not self.instance:
            self.instance = super(Singleton, self).__call__(*args, **kwargs)

        return self.instance
