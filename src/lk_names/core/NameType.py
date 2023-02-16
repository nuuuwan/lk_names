from lk_names.core.NAME_TO_TYPE import NAME_TO_TYPE, TYPE_TO_NAMES

NAME_TYPE_UNKNOWN = 'unknown'


class NameType:
    @staticmethod
    def get(name):
        return NAME_TO_TYPE.get(name, NAME_TYPE_UNKNOWN)

    @staticmethod
    def list_all():
        return list(sorted(TYPE_TO_NAMES.keys())) + [NAME_TYPE_UNKNOWN]
