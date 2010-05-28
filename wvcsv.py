from _wvcsv import *

class CsvReader:
    def __init__(self, data):
        self.id = csvsetup(data);

    def __iter__(self):
        while True:
            r = csvreadline(self.id)
            if r is None:
                break
            yield r

    def __del__(self):
        csvtakedown(self.id)
