from lk_names.core.UniqueNames import UniqueNames
from fuzzywuzzy import fuzz
from lk_names import FiledVariable
from utils import Log
import time

log = Log('NormalizedNames')


class NormalizedNames:
    MIN_SIMILARITY_FOR_MATRIX = 0.7

    @staticmethod
    def similarity(name1, name2):
        return fuzz.ratio(name1, name2) / 100.0

    @staticmethod
    def similarity_matrix():
        def nocache():
            matrix = {}
            unique_names = UniqueNames.list_all()
            n = len(unique_names)
            n_pairs = n * (n - 1) // 2
            i_pair = 0
            n_pairs_in_matrix = 0
            t0 = time.time()
            for i in range(n):
                name_i = unique_names[i]
                for j in range(i + 1, n):
                    i_pair += 1
                    name_j = unique_names[j]

                    similarity = NormalizedNames.similarity(name_i, name_j)
                    if similarity < NormalizedNames.MIN_SIMILARITY_FOR_MATRIX:
                        continue

                    if i not in matrix:
                        matrix[i] = {}
                    matrix[i][j] = similarity
                    n_pairs_in_matrix += 1

                    if n_pairs_in_matrix % 10_000 != 0:
                        continue
                    p_pairs = i_pair / n_pairs
                    dt = time.time() - t0
                    t_total = dt / p_pairs

                    log.debug(
                        f'{p_pairs:.1%} ({dt:.0f}s/{t_total:.0f}s)'
                        + f'\t{n_pairs_in_matrix:,}'
                        + f' "{name_i}" x "{name_j}" = {similarity:.0%}'
                    )

            log.debug(f'Stored {n_pairs_in_matrix:,}/{n_pairs:,} pairs')
            return matrix

        return FiledVariable('data/similarity_matrix.json', nocache).get()

    def similarity_matrix_pruned(similarity_limit):
        def nocache():
            matrix = NormalizedNames.similarity_matrix()
            matrix_pruned = {}
            for i in matrix:
                for j in matrix[i]:
                    if matrix[i][j] < similarity_limit:
                        continue
                    if i not in matrix_pruned:
                        matrix_pruned[i] = {}
                    matrix_pruned[i][j] = matrix[i][j]
            return matrix_pruned

        return FiledVariable(
            f'data/similarity_matrix-{similarity_limit:.2f}.json', nocache
        ).get()

    @staticmethod
    def similar_clusters(similarity_limit):
        def nocache():
            name_to_count = UniqueNames.name_to_count()
            idx = UniqueNames.idx()
            similarity_matrix = NormalizedNames.similarity_matrix_pruned(
                similarity_limit
            )

            def is_similar_enough(i, j):
                i = str(i)
                j = str(j)
                if i in similarity_matrix and j in similarity_matrix[i]:
                    return True
                if j in similarity_matrix and i in similarity_matrix[j]:
                    return True
                return False

            clusters = {}
            n = len(name_to_count)
            i_visited = 0
            for name in name_to_count.keys():
                i = idx[name]
                i_visited += 1
                found_existing_cluster = False
                for j in clusters:
                    if is_similar_enough(i, j):
                        clusters[j].append(i)

                        print(f'\t\t{i_visited}/{n} {i} -> {j}', end='\r')
                        found_existing_cluster = True
                        break
                if not found_existing_cluster:
                    clusters[i] = []

            return clusters

        return FiledVariable(
            f'data/similar_clusters-{similarity_limit:.02f}.json', nocache
        ).get()

    def similar_cluster_idx(similarity_limit):
        def nocache():
            clusters = NormalizedNames.similar_clusters(similarity_limit)
            cluster_idx = {}
            for i in clusters:
                cluster_idx[i] = i
                for j in clusters[i]:
                    cluster_idx[j] = i
            return cluster_idx

        return FiledVariable(
            f'data/similar_cluster_idx-{similarity_limit:.02f}.json', nocache
        ).get()

    @staticmethod
    def name_to_count_for_type(similarity_limit, name_type):
        def nocache():
            name_to_count = NormalizedNames.similar_cluster_idx(
                similarity_limit
            )
            name_to_count_for_type = {}
            for name, count in name_to_count:
                if name in TYPE_TO_NAME[name_type]:
                    name_to_count_for_type[name] = count
            return name_to_count_for_type

        return FiledVariable(
            f'data/name_to_count_for_type-{similarity_limit:.02f}-{name_type}.json',
            nocache,
        ).get()


if __name__ == '__main__':
    NormalizedNames.similarity_matrix()
    NormalizedNames.similarity_matrix_pruned(0.8)
    NormalizedNames.similarity_matrix_pruned(0.9)
    NormalizedNames.similarity_matrix_pruned(0.95)
    NormalizedNames.similar_clusters(0.9)
    NormalizedNames.similar_cluster_idx(0.9)
    NormalizedNames.name_to_count_for_type(0.85, 'stop')
