import _wvcsv

dequote = _wvcsv.dequote
quote = _wvcsv.quote


def quotel(v):
    return ','.join(quote(i) for i in v) + '\r\n'


class Reader:
    def __init__(self, data):
        self.id = _wvcsv.setup(data);

    def __iter__(self):
        while True:
            r = _wvcsv.readline(self.id)
            if r is None:
                break
            yield _wvcsv.splitline(r)

    def __del__(self):
        _wvcsv.takedown(self.id)
