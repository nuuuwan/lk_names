from lk_names.core.NAME_TO_TYPE import NAME_TO_TYPE, TYPE_TO_NAMES
from lk_names.core.UniqueNames import UniqueNames
from lk_names import FiledVariable
from gig import Ent, EntType

NAME_TYPE_UNKNOWN = 'unknown'


class NameType:
    @staticmethod
    def get(name):
        return NAME_TO_TYPE.get(name, NAME_TYPE_UNKNOWN)

    @staticmethod
    def list_all():
        return list(sorted(TYPE_TO_NAMES.keys())) + [NAME_TYPE_UNKNOWN]

    @staticmethod
    def unknown_names():
        def nocache():
            unknown_set = set()
            for district_ent in Ent.list_from_type(EntType.DISTRICT):
                district_id = district_ent.id
                name_to_count_original = UniqueNames.name_to_count(
                    district_id
                )
                for name, count in list(name_to_count_original.items())[:10]:
                    name_type = NameType.get(name)
                    if name_type == NAME_TYPE_UNKNOWN:
                        unknown_set.add(name)
            return list(sorted(unknown_set))

        return FiledVariable('data/unknown_names.json', nocache).get(
            force=True
        )


if __name__ == '__main__':
    NameType.unknown_names()
