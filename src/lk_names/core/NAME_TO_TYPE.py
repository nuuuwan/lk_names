TYPE_TO_NAMES = {
    'stop': [
        'mudiyanselage',
        'arachchige',
        'gedara',
        'don',
        'kankanamge',
        'kumari',
        'kumara',
        'arachchilage',
        'pedige',
        'ralalage',
        'appuhamilage',
        'hetti',
        'pathirannehelage',
        'mudalige',
    ],
    'surname': [
        'perera',
        'bandara',
        'herath',
        'fernando',
        'gamage',
        'dissanayaka',
        'rathnayaka',
        'liyanage',
        'rajapaksha',
        'de-silva',
        'ranasinghe',
        'silva',
        'jayasinghe',
        'hewa',
        'hewage',
        'weerasinghe',
        'amarasinghe',
        'warnakulasooriya',
        'vithanage',
        'pathiranage',
        'wickramasinghe',
        'karunarathna',
        'jayalath',
        'dewage',
        'ekanayaka',
        'thennakoon',
        'jayarathna',
        'wijesinghe',
        
    ],
    'first-name-male': [
        'mohamad',
        'priyantha',
        'nishantha',
        'chaminda',
        'wasantha',
        'sampath',
        'sarath',
        'abdul',
        'pradeep',
        'muhammadu',
        'indika',
        'ajith',
        'saman',
        'sanjeewa',
        'ranjith',
        'chandana',
        'nimal',
        'gamini',
        'sunil',
        'roshan',
        'ruwan',
        'mohamed',
        'samantha',
        'dhammika',
        'jayantha',
        'prasanna',
        'anura',
        'janaka',
        'mohomad',
        'lakmal',
        'ananda',
        'prasad',
        'mohomed',
        'thushara',
        'manjula',
        'upul',
        'susantha',
        
    ],
    'first-name-female': [
        'priyadarshani',
        'pushpa',
        'fathima',
        'damayanthi',

    ],
    'fist-name-unisex': {
        'chandra',
    }
}

NAME_TO_TYPE = {}
for type, names in TYPE_TO_NAMES.items():
    for name in names:
        NAME_TO_TYPE[name] = type