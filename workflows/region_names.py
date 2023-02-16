from gig import Ent, EntType


def count_chars(name, c):
    n_c = sum(1 for char in name if char == c)
    len(name)
    return n_c


def get_names():
    names = []
    for ent_type in [
        EntType.GND,
        EntType.DSD,
        EntType.DISTRICT,
        EntType.PROVINCE,
    ]:
        ents = Ent.list_from_type(ent_type)
        names += [ent.name for ent in ents]
    return names


def main():
    names = get_names()

    c_to_names = {}
    for name in names:
        name = name.upper()
        # name = name.replace('-', '')
        # name = name.upper().split(' ')[0]

        c = name[0]
        if c not in c_to_names:
            c_to_names[c] = []
        c_to_names[c].append(name)

    for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        names_for_c = c_to_names.get(c)
        if not names_for_c:
            print(f'{c}\t-')
            continue

        names_for_c = sorted(
            names_for_c,
            key=lambda name: count_chars(name, c) * 10000 - len(name),
            reverse=True,
        )
        selected_name = names_for_c[0].title()
        print(f'{c}\t{selected_name}')


if __name__ == '__main__':
    main()
