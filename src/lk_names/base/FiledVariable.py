import os

from utils import JSONFile, Log

log = Log('FiledVariable')


class FiledVariable:
    def __init__(self, path, func_get):
        self.path = path
        self.func_get = func_get

    def get(self, force=False):
        file = JSONFile(self.path)
        if file.exists and not force:
            return file.read()

        value = self.func_get()
        file.write(value)
        file_size = os.path.getsize(self.path)
        log.debug(f'Wrote {self.path} ({file_size:,}B)')
        return value
