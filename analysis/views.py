from io import StringIO, BytesIO
import zipfile
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, StreamingHttpResponse, HttpResponse
from django.shortcuts import render
from analysis.models import MusicData, Composition
from analysis.computation import ambitus
from analysis.computation import intervals
from analysis.computation import durations
from analysis.computation import contour
from analysis.computation import pure_data
from analysis.computation import cluster


def home(request):
    return render(request, "index.html")


def login_user(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, "login_user.html", {'error': True})
        else:
            return render(request, "login_user.html", {'error': True})

    else:
        return render(request, 'login_user.html')


def dashboard(request):
    music_data_count = MusicData.objects.count()
    composition_count = Composition.objects.count()
    args = {'music_data_count': music_data_count,
            'composition_count': composition_count}
    return render(request, "dashboard.html", args)


def uniq_items_in_model(item, model=MusicData):
    items = model.objects.values(item).distinct().order_by(item)
    return [x[item] for x in items]


def select_filter(name, item, arguments, template='music_data__%s'):
    if item != "all":
        arguments[template % name] = item


def show_ambitus(request):


    if request.method == 'POST':
        kwargs = {}

        title = request.POST['select-composition']
        key = request.POST['select-key']
        total_duration = request.POST['select-duration']
        time_signature = request.POST['select-time-signature']

        select_filter('title__iexact', title, kwargs, template='%s')
        select_filter('key', key, kwargs)
        select_filter('total_duration', total_duration, kwargs)
        select_filter('time_signature', time_signature, kwargs)

        compositions = Composition.objects.filter(**kwargs)
        args = ambitus.analysis(compositions)
        return render(request, 'ambitus_result.html', args)

    args = {'compositions': uniq_items_in_model('title', Composition),
            'keys': uniq_items_in_model('key'),
            'durations': uniq_items_in_model('total_duration'),
            'signatures': uniq_items_in_model('time_signature'),
    }
    return render(request, 'ambitus.html', args)


def show_intervals(request):
    if request.method == 'POST':
        kwargs = {}

        title = request.POST['select-composition']
        key = request.POST['select-key']
        total_duration = request.POST['select-duration']
        time_signature = request.POST['select-time-signature']

        select_filter('title__iexact', title, kwargs, template='%s')
        select_filter('key', key, kwargs)
        select_filter('total_duration', total_duration, kwargs)
        select_filter('time_signature', time_signature, kwargs)

        compositions = Composition.objects.filter(**kwargs)
        args = intervals.analysis(compositions)
        return render(request, 'intervals_result.html', args)

    args = {'compositions': uniq_items_in_model('title', Composition),
            'keys': uniq_items_in_model('key'),
            'durations': uniq_items_in_model('total_duration'),
            'signatures': uniq_items_in_model('time_signature'),
            }

    return render(request, 'intervals.html', args)

def show_durations(request):
    if request.method == 'POST':
        kwargs = {}

        title = request.POST['select-composition']
        key = request.POST['select-key']
        time_signature = request.POST['select-time-signature']

        select_filter('title__iexact', title, kwargs, template='%s')
        select_filter('key', key, kwargs)
        select_filter('time_signature', time_signature, kwargs)

        compositions = Composition.objects.filter(**kwargs)
        args = durations.analysis(compositions)
        return render(request, 'durations_result.html', args)

    args = {'compositions': uniq_items_in_model('title', Composition),
            'keys': uniq_items_in_model('key'),
            'signatures': uniq_items_in_model('time_signature'),
            }

    return render(request, 'durations.html', args)

def show_contour(request):
    if request.method == 'POST':
        kwargs = {}

        title = request.POST['select-composition']
        key = request.POST['select-key']
        total_duration = request.POST['select-duration']
        time_signature = request.POST['select-time-signature']

        select_filter('title__iexact', title, kwargs, template='%s')
        select_filter('key', key, kwargs)
        select_filter('total_duration', total_duration, kwargs)
        select_filter('time_signature', time_signature, kwargs)

        compositions = Composition.objects.filter(**kwargs)
        args = contour.analysis(compositions)
        return render(request, 'contour_result.html', args)

    args = {'compositions': uniq_items_in_model('title', Composition),
            'keys': uniq_items_in_model('key'),
            'durations': uniq_items_in_model('total_duration'),
            'signatures': uniq_items_in_model('time_signature'),
    }
    return render(request, 'contour.html', args)


def show_pure_data(request):
    if request.method == 'POST':
        kwargs = {}

        title = request.POST['select-composition']
        key = request.POST['select-key']
        total_duration = request.POST['select-duration']
        time_signature = request.POST['select-time-signature']
        markov_order = request.POST['select-markov-order']

        select_filter('title__iexact', title, kwargs, template='%s')
        select_filter('key', key, kwargs)
        select_filter('total_duration', total_duration, kwargs)
        select_filter('time_signature', time_signature, kwargs)

        compositions = Composition.objects.filter(**kwargs)
        args = pure_data.analysis(compositions, order=int(markov_order))

        buff = BytesIO()
        zip_archive = zipfile.ZipFile(buff, mode='w')

        for key, value in args.items():
            zip_archive.writestr(key + '.coll', "".join(value))

        zip_archive.close()

        response = HttpResponse(buff.getvalue(), mimetype="application/x-zip-compressed")
        response['Content-Disposition'] = 'attachment; filename=%s' % "markov-chains.zip"
        return response

    args = {'compositions': uniq_items_in_model('title', Composition),
            'keys': uniq_items_in_model('key'),
            'durations': uniq_items_in_model('total_duration'),
            'signatures': uniq_items_in_model('time_signature'),
            'order_numbers': range(1, 11)
            }
    return render(request, 'pure_data.html', args)


def show_cluster(request):
    if request.method == 'POST':
        kwargs = {}

        title = request.POST['select-composition']
        key = request.POST['select-key']
        total_duration = request.POST['select-duration']
        time_signature = request.POST['select-time-signature']

        select_filter('title__iexact', title, kwargs, template='%s')
        select_filter('key', key, kwargs)
        select_filter('total_duration', total_duration, kwargs)
        select_filter('time_signature', time_signature, kwargs)

        compositions = Composition.objects.filter(**kwargs)
        args = cluster.analysis(compositions)
        return render(request, 'cluster_result.html', args)

    args = {'compositions': uniq_items_in_model('title', Composition),
            'keys': uniq_items_in_model('key'),
            'durations': uniq_items_in_model('total_duration'),
            'signatures': uniq_items_in_model('time_signature'),
    }
    return render(request, 'cluster.html', args)


def stats(request):
    args = {
        'number_music_data': MusicData.objects.count(),
        'number_compositions': Composition.objects.count(),
    }
    return render(request, 'stats.html', args)
