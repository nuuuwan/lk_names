from dataclasses import dataclass

from utils import JSONFile
from lk_names import FiledVariable


@dataclass
class Person:
    lg_id: str
    district_id: str
    name: str

    MIN_NAME_LENGTH = 2

    @property
    def cleaned_name(self):
        cleaned_name = ''.join(
            [c if c.isalpha() else ' ' for c in self.name.lower()]
        )
        # De Silva etc
        if cleaned_name[:3] == 'de ':
            cleaned_name = 'de-' + cleaned_name[3:]
        cleaned_name = cleaned_name.replace(' de ', ' de-')
        return cleaned_name

    @property
    def names(self):
        names = self.cleaned_name.split(' ')
        names = [n for n in names if len(n) >= self.MIN_NAME_LENGTH]
        return names

    @staticmethod
    def from_dict(d):
        return Person(
            d['lg_id'],
            d['district_id'],
            d['name'],
        )

    @staticmethod
    def list_all():
        d_list = JSONFile('data/lgelecsl_2023/candidates.json').read()
        return [Person.from_dict(d) for d in d_list]

    @staticmethod
    def region_to_count():
        def nocache():
            region_to_count = {}
            for p in Person.list_all():
                region_to_count[p.district_id] = (
                    region_to_count.get(p.district_id, 0) + 1
                )
                region_to_count[p.lg_id] = region_to_count.get(p.lg_id, 0) + 1
            return region_to_count

        return FiledVariable('data/region_to_count.json', nocache).get()


if __name__ == '__main__':
    Person.region_to_count()
