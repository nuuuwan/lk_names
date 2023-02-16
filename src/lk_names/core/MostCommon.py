from lk_names import FiledVariable
from lk_names.core.UniqueNames import UniqueNames
from lk_names.core.NameType import NameType
from lk_names.core.NormalizedNames import NormalizedNames
from gig import Ent, EntType

class MostCommon:
    @staticmethod
    def name_to_count(region_id, similarity_limit):
        def nocache():
            name_to_count_original = UniqueNames.name_to_count(region_id)
            similar_cluster_idx = NormalizedNames.similar_cluster_idx(
                similarity_limit
            )
            unique_names = UniqueNames.list_all()
            idx = UniqueNames.idx()

            name_to_count ={}
            for name, count in name_to_count_original.items():
                i_name = idx[name]
                i_cluster = int(similar_cluster_idx[str(i_name)])
                cluster_name = unique_names[i_cluster]
                name_to_count[cluster_name] = (
                    name_to_count.get(cluster_name, 0) + count
                )
            name_to_count = dict(
                sorted(
                    name_to_count.items(), key=lambda x: x[1], reverse=True
                )
            )
            return name_to_count

        return FiledVariable(
            f'data/most_common/name_to_count/{region_id}-{similarity_limit:.02f}.json',
            nocache,
        ).get()

    @staticmethod
    def name_to_count_from_type(region_id, name_type, similarity_limit):
        def nocache():
            name_to_count = MostCommon.name_to_count(region_id, similarity_limit)
            name_to_count_from_type = {}
            for name, count in name_to_count.items():
                name_type2 = NameType.get(name)
                if name_type == name_type2:
                    name_to_count_from_type[name] = count
            return name_to_count_from_type

        return FiledVariable(
            'data/most_common/name_to_count'+f'/{region_id}-{name_type}-{similarity_limit:.02f}.json',
            nocache,
        ).get(force=True)

    

    


if __name__ == '__main__':
    SIMILARITY_LIMIT = 0.85
    for name_type in NameType.list_all():
        MostCommon.name_to_count_from_type('LK', name_type, SIMILARITY_LIMIT)

    for ent_type in [EntType.DISTRICT]:
        ent_list = Ent.list_from_type(ent_type)
        for ent in ent_list:
            region_id = ent.id
            for name_type in NameType.list_all():    
                MostCommon.name_to_count_from_type(region_id, name_type, SIMILARITY_LIMIT)
