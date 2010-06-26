from _wvcsv import *

class Reader:
    def __init__(self, data):
        self.id = setup(data);

    def __iter__(self):
        while True:
            r = readline(self.id)
            if r is None:
                break
            yield r

    def __del__(self):
        takedown(self.id)
