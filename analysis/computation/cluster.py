import numpy
from analysis.computation import utils


def get_duration_ambitus(compositions, normalize=True):
    pairs = [(c.music_data.total_duration, c.music_data.ambitus) for c in compositions]
    if normalize:
        arr = numpy.array(pairs)
        for i in 0, 1:
            arr = utils.normalize_array(arr, i)
        pairs = arr.tolist()

    pairs.insert(0, ['', 'Piece'])
    return pairs


def analysis(compositions):
    duration_ambitus = get_duration_ambitus(compositions)

    if duration_ambitus:
        args = {
            'duration_ambitus': duration_ambitus,
        }
    else:
        args = {}

    return args
