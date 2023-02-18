from lk_names.core.NameType import NameType
from lk_names.core.MostCommon import MostCommon
from lk_names import FiledVariable
from gig import Ent, EntType
from utils import File

NAME_TYPE_UNKNOWN = 'unknown'

SIMILARITY_LIMIT = 0.85


class NameTypeAndMostCommon:
    @staticmethod
    def unknown_names():
        def nocache():
            unknown_set = set()
            for district_ent in Ent.list_from_type(EntType.DISTRICT):
                district_id = district_ent.id
                name_to_count_original = MostCommon.name_to_count(
                    district_id, SIMILARITY_LIMIT
                )
                for name, count in list(name_to_count_original.items())[:50]:
                    name_type = NameType.get(name)
                    if name_type == NAME_TYPE_UNKNOWN:
                        unknown_set.add(name)
            return list(sorted(unknown_set))

        unknown_names = FiledVariable(
            'data/name_types/unknown_names.json', nocache
        ).get(force=True)
        File('data/name_types/unknown_names.txt').write_lines(unknown_names)


if __name__ == '__main__':

    NameTypeAndMostCommon.unknown_names()
