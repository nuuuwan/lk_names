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


if __name__ == '__main__':
    NormalizedNames.similarity_matrix()
    NormalizedNames.similarity_matrix_pruned(0.8)
    NormalizedNames.similarity_matrix_pruned(0.9)
    NormalizedNames.similarity_matrix_pruned(0.95)
