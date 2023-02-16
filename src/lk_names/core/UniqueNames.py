from lk_names import FiledVariable
from lk_names.core.Person import Person


class UniqueNames:
    @staticmethod
    def list_all():
        def nocache():
            all_names = []
            for person in Person.list_all():
                all_names += person.names
            return list(sorted(set(all_names)))

        return FiledVariable('data/unique_names.json', nocache).get(
            force=True
        )


if __name__ == '__main__':
    UniqueNames.list_all()
