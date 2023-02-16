from lk_names import FiledVariable
from lk_names.core.UniqueNames import UniqueNames
from lk_names.core.NameType import NameType
from lk_names.core.NormalizedNames import NormalizedNames
from gig import EntType, Ent
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os


rcParams['font.family'] = 'Gill Sans'

SIMILARITY_LIMIT = 0.85

alpha = 0.2
colors = [
    (0.5, 0.0, 0.0, alpha),
    (1, 0.5, 0.0, alpha),
    (0, 0.5, 0.0, alpha),
    (1, 1, 0.0, alpha),
    (0.5, 0.5, 0.5, alpha),
    (0, 0.5, 1.0, alpha),
    (0, 0.0, 0.5, alpha),
]
n_colors = len(colors)
i_color = 0

NAME_TO_COLOR = {}


def get_color(name):
    global i_color
    if name not in NAME_TO_COLOR:
        NAME_TO_COLOR[name] = colors[i_color]
        i_color += 1
        if i_color >= n_colors:
            i_color = 0
    return NAME_TO_COLOR[name]


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

            name_to_count = {}
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
            name_to_count = MostCommon.name_to_count(
                region_id, similarity_limit
            )
            name_to_count_from_type = {}
            for name, count in name_to_count.items():
                name_type2 = NameType.get(name)
                if name_type == name_type2:
                    name_to_count_from_type[name] = count
            return name_to_count_from_type

        dir = 'data/most_common/name_to_count' + f'/{name_type}'
        if not os.path.exists(dir):
            os.makedirs(dir)

        return FiledVariable(
            'data/most_common/name_to_count'
            + f'/{name_type}/{region_id}-{similarity_limit:.02f}.json',
            nocache,
        ).get(force=True)

    @staticmethod
    def draw_map_for_name_from_type(name_type, similarity_limit):
        _, ax = plt.subplots(figsize=(16, 9))
        ent_list = Ent.list_from_type(EntType.DISTRICT)
        for ent in ent_list:
            region_id = ent.id
            name_to_count = MostCommon.name_to_count_from_type(
                region_id, name_type, similarity_limit
            )
            if name_to_count:
                most_common_name = list(name_to_count.keys())[0]
                color = get_color(most_common_name)
                geo = ent.geo()
                geo.plot(ax=ax, color=color)
                xy = ent.centroid[1], ent.centroid[0]
                plt.annotate(most_common_name, xy, ha='center')

        png_file_name = (
            'images/most_common/name_to_count'
            + f'/{name_type}-{similarity_limit:.02f}.png'
        )
        plt.savefig(png_file_name)
        plt.close()
        os.system(f'open -a firefox "{png_file_name}"')


if __name__ == '__main__':
    MostCommon.draw_map_for_name_from_type(
        'first-name-male', SIMILARITY_LIMIT
    )
