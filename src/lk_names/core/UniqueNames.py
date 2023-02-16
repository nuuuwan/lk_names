from lk_names import FiledVariable
from lk_names.core.Person import Person
from gig import Ent, EntType


class UniqueNames:
    @staticmethod
    def name_to_count(region_id='LK'):
        def nocache():
            name_to_count = {}
            for person in Person.list_all():
                district_id = person.district_id
                if region_id not in district_id:
                    continue
                for name in person.names:
                    if name not in name_to_count:
                        name_to_count[name] = 0
                    name_to_count[name] += 1

            name_to_count = dict(
                sorted(
                    name_to_count.items(), key=lambda x: x[1], reverse=True
                )
            )

            return name_to_count

        return FiledVariable(
            f'data/name_to_count/{region_id}.json', nocache
        ).get()

    @staticmethod
    def list_all():
        def nocache():
            name_to_count = UniqueNames.name_to_count()
            return sorted(name_to_count.keys())

        return FiledVariable('data/unique_names/list_all.json', nocache).get()

    @staticmethod
    def idx():
        def nocache():
            return {name: i for i, name in enumerate(UniqueNames.list_all())}

        return FiledVariable('data/unique_names/idx.json', nocache).get(
            force=True
        )


if __name__ == '__main__':
    UniqueNames.name_to_count()
    UniqueNames.list_all()
    UniqueNames.idx()

    for ent_type in [EntType.DISTRICT, 'LK']:
        ent_list = Ent.list_from_type(ent_type)
        for ent in ent_list:
            region_id = ent.id
            UniqueNames.name_to_count(region_id)
