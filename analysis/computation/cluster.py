import numpy
from analysis.computation import utils


def get_duration_ambitus(compositions, normalize=True, labelize=False):
    pairs = [(c.music_data.total_duration, c.music_data.ambitus) for c in compositions]
    if normalize:
        arr = numpy.array(pairs)
        for i in 0, 1:
            arr = utils.normalize_array(arr, i)
        pairs = arr.tolist()

    if labelize:
        seq = []
        for i in range(len(pairs)):
            imslp = compositions[i].collection.imslp_id
            row = []
            x, y = pairs[i]
            row.append({'v': x, 'f':'{}. {}'.format(imslp, x)})
            row.append(y)

            seq.append(row)

        pairs = seq

    pairs.insert(0, ['', 'Piece'])
    return pairs


def duration_ambitus_cluster(duration_ambitus):
    array = numpy.array(duration_ambitus[1:])
    return utils.make_optics_plot_data(array)


def duration_reachability(array):
    min_pts = 10

    if len(array) < 10:
        min_pts = 0

    reachability_plot = utils.make_reachability_plot_data(array, min_pts)

    reachability_plot.insert(0, ['Piece', 'Reachability value'])
    return reachability_plot


def make_clusters(compositions, array):
    leaves = utils.get_optics_data(array)[-1]

    clusters = []

    for leave_number, leave in enumerate(leaves):
        l_dic = {}
        l_dic['number'] = leave_number
        l_dic['size'] = len(leave.order)
        songs = []
        for n in leave.order:
            composition = compositions.get(id=n)
            title = composition.title
            code = composition.music_data.score.code
            songs.append({'title': title, 'code': code, 'first': False})

        songs[0]['first'] = True
        l_dic['songs'] = songs


        clusters.append(l_dic)

    return clusters




def analysis(compositions):
    duration_ambitus_label = get_duration_ambitus(compositions, True, True)
    duration_ambitus = get_duration_ambitus(compositions, True, False)
    cluster = duration_ambitus_cluster(duration_ambitus)

    array = numpy.array(duration_ambitus[1:])

    reachability_plot = duration_reachability(array)
    cluster_table = make_clusters(compositions, array)

    if duration_ambitus:
        args = {
            'duration_ambitus_label': duration_ambitus_label,
            'duration_ambitus': duration_ambitus,
            'cluster': cluster,
            'reachability_plot': reachability_plot,
            'cluster_table': cluster_table,
        }
    else:
        args = {}

    return args