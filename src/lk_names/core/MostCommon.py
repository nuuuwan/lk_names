from lk_names import FiledVariable
from lk_names.core.UniqueNames import UniqueNames
from lk_names.core.NameType import NameType
from lk_names.core.NormalizedNames import NormalizedNames
from lk_names.core.Person import Person
from gig import EntType, Ent
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os
import math


rcParams['font.family'] = 'Gill Sans'

SIMILARITY_LIMIT = 0.85

alpha = 0.3
colors = [
    (0.5, 0.0, 0.0, alpha),
    (1, 0.5, 0.0, alpha),
    (0, 0.5, 0.0, alpha),
    (1, 1, 0.0, alpha),
    (0.5, 0.5, 0.5, alpha),
    (0, 0.5, 1.0, alpha),
    (0, 0.0, 0.5, alpha),
    (0.5, 0.0, 0.0, alpha / 2),
    (1, 0.5, 0.0, alpha / 2),
    (0, 0.5, 0.0, alpha / 2),
    (1, 1, 0.0, alpha / 2),
    (0.5, 0.5, 0.5, alpha / 2),
    (0, 0.5, 1.0, alpha / 2),
    (0, 0.0, 0.5, alpha / 2),
]
n_colors = len(colors)
i_color = 0

NAME_TO_COLOR = {}


def get_color_for_p(p, max_p):
    if p == 0 :
        return 'white'
    base = math.log2(max_p)
    log_p = math.log2(p)
    if log_p > base-1:
        return ((0.5, 0.0, 0.0, alpha),)
    if log_p > base-2:
        return (1, 0.5, 0.0, alpha)
    if log_p > base-3:
        return (1, 1, 0.0, alpha)
    if log_p > base-4:
        return (0, 0.5, 0.0, alpha)
    return (0, 0.5, 1.0, alpha)


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
        ).get(force=False)

    @staticmethod
    def draw_map_for_name_from_type(name_type, similarity_limit):
        _, ax = plt.subplots(figsize=(6.75, 12))

        ent_list = Ent.list_from_type(EntType.DISTRICT)
        for ent in ent_list:
            region_id = ent.id
            name_to_count = MostCommon.name_to_count_from_type(
                region_id, name_type, similarity_limit
            )
            if name_to_count:
                label = list(name_to_count.keys())[0].title()
                color = get_color(label)
            else:
                color = '#f0f0f0'
                label = '(no data)'
            geo = ent.geo()
            geo.plot(ax=ax, color=color, edgecolor='#ccc')
            xy = ent.centroid[1], ent.centroid[0]
            plt.annotate(label, xy, ha='center')

        ax.grid(False)
        # Hide axes ticks
        ax.set_xticks([])
        ax.set_yticks([])

        plt.title(name_type)

        png_file_name = (
            'images/most_common/name_to_count'
            + f'/{name_type}-{similarity_limit:.02f}.png'
        )
        plt.savefig(png_file_name)
        plt.close()
        os.system(f'open -a firefox "{png_file_name}"')

    @staticmethod
    def draw_map_for_name(selected_name, similarity_limit):
        region_to_count = Person.region_to_count()
        similar_cluster_idx = NormalizedNames.similar_cluster_idx(
            similarity_limit
        )
        unique_names = UniqueNames.list_all()
        idx = UniqueNames.idx()
        i_selected_name = idx[selected_name.lower()]
        i_selected_name_cluster = int(
            similar_cluster_idx[str(i_selected_name)]
        )
        cluster_name = unique_names[i_selected_name_cluster]

        _, ax = plt.subplots(figsize=(6.75, 12))

        ent_list = Ent.list_from_type(EntType.DISTRICT)
        region_to_p = {}
        max_p = 0
        for ent in ent_list:
            region_id = ent.id
            name_to_count = MostCommon.name_to_count(
                region_id, similarity_limit
            )
            n_name = name_to_count.get(cluster_name, 0)
            n_total = region_to_count.get(region_id, 0)

            if n_total > 0:
                p_name = n_name / n_total
                max_p = max(max_p, p_name)
            else:
                p_name = None

            region_to_p[region_id] = p_name
            
        
        for ent in ent_list:
            region_id = ent.id
            p = region_to_p[region_id]
            if p is not None:
                if p == 0:
                    label = 'none'
                elif p < 0.001:
                    label = f'<1 in 1,000'
                else:
                    r = 1 / p
                    label = f'1 in {r:,.0f}'
                color = get_color_for_p(p, max_p)
            else:
                label = '(no data)'
                color = '#f0f0f0'

            geo = ent.geo()
            geo.plot(ax=ax, color=color, edgecolor='#ccc')
            xy = ent.centroid[1], ent.centroid[0]
            plt.annotate(label, xy, ha='center')

        ax.grid(False)
        # Hide axes ticks
        ax.set_xticks([])
        ax.set_yticks([])

        plt.title(cluster_name.title())

        png_file_name = (
            'images/most_common/name_to_count'
            + f'/name.{cluster_name}-{similarity_limit:.02f}.png'
        )
        plt.savefig(png_file_name)
        plt.close()
        os.system(f'open -a firefox "{png_file_name}"')


if __name__ == '__main__':
    for name_type in NameType.list_all():
        MostCommon.draw_map_for_name_from_type(name_type, SIMILARITY_LIMIT)

        name_to_count_from_type = MostCommon.name_to_count_from_type('', name_type, SIMILARITY_LIMIT)

        for name, count in list(name_to_count_from_type.items())[:3]:
            MostCommon.draw_map_for_name(name, SIMILARITY_LIMIT)

    
    
