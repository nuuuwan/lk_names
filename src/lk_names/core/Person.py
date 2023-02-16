from dataclasses import dataclass

from utils import JSONFile


@dataclass
class Person:
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
            d['district_id'],
            d['name'],
        )

    @staticmethod
    def list_all():
        d_list = JSONFile('data/lgelecsl_2023/candidates.json').read()
        return [Person.from_dict(d) for d in d_list]
