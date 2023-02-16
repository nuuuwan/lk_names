from lk_names import FiledVariable
from utils import Directory

NAME_TYPE_UNKNOWN = 'unknown'


class NameType:
    @staticmethod
    def get_type_to_names():
        def nocache():
            type_to_names = {}
            for file in Directory('data/name_types/ground_truth').children:
                type_to_names[file.name[:-4]] = [
                    line.strip() for line in file.read_lines() if line.strip()
                ]
            return type_to_names

        return FiledVariable(
            'data/name_types/type_to_names.json', nocache
        ).get(force=False)

    @staticmethod
    def get_name_to_type():
        def nocache():
            type_to_names = NameType.get_type_to_names()
            name_to_type = {}
            for type, names in type_to_names.items():
                for name in names:
                    name_to_type[name] = type
            return name_to_type

        return FiledVariable(
            'data/name_types/name_to_type.json', nocache
        ).get(force=False)

    @staticmethod
    def get(name):
        name_to_type = NameType.get_name_to_type()
        return name_to_type.get(name, NAME_TYPE_UNKNOWN)

    @staticmethod
    def list_all():
        type_to_names = NameType.get_type_to_names()
        return list(sorted(type_to_names.keys())) + [NAME_TYPE_UNKNOWN]


if __name__ == '__main__':
    NameType.get_type_to_names()
    NameType.get_name_to_type()
