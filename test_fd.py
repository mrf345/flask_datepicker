from flask import Flask, render_template
from flask_datepicker import datepicker
from os import path, mkdir
from shutil import rmtree
from pytest import fixture
from atexit import register
from random import randint
from tempfile import TemporaryFile
from json import loads
from sys import version_info as V
if V.major == 2:
    FileNotFoundError = IOError


dirs = ['templates', 'static']

def toCleanUp():
    for d in dirs:
        if path.isdir(d):
            rmtree(d)

register(toCleanUp)

def toMimic(data, static=False):
    for d in dirs:
        if not path.isdir(d):
            mkdir(d)
    while True:
        tFile = str(randint(1, 9999999)) + (
            data if static else '.html')
        if not path.isfile(tFile):
            break
    with open(
        path.join(
            dirs[1] if static else dirs[0], tFile
            ), 'w+') as file:
        file.write(data)
    return tFile


app = Flask(__name__)
eng = datepicker(app, local=[])


@app.route('/loader')
def loader():
    return render_template(
        toMimic("{{ datepicker.loader() }}")
    )

@app.route('/picker')
def picker():
    return render_template(
        toMimic("{{ datepicker.picker() }}")
    )

@app.route('/min_max/<min>/<max>')
def minMax(min, max):
    return render_template(
        toMimic(
            """
            <html>
                <head>
                    <script
                    src="https://code.jquery.com/jquery-3.3.1.min.js"
                    ></script>
                    {{ datepicker.loader() }}
                    {{ datepicker.picker(minDate='%s', maxDate='%s') }}
                </head>
                <body>
                    <input class='datepicker'>
                </body>
            </html>
            """ % (min, max)
        )
    )

@fixture
def client():
    app.config['TESTING'] = True
    app.config['STATIC_FOLDER'] = 'static'
    app.config['SERVER_NAME'] = 'localhost'
    client = app.test_client()
    yield client


def test_loader_template_links(client):
    resp = client.get('/loader').data
    for link in [
        'jquery-ui.min.js',
        'jquery-ui.css'
        ]:
        assert link.encode('utf8') in resp


def test_picker_template_script(client):
    resp = client.get('/picker').data
    assert 'var toF = this; $(this).datepicker({'.encode('utf8') in resp

def test_picker_min_max_dates(client):
    dates = ['2018-07-03', '2019-07-03']
    resp = client.get('/min_max/%s/%s' % (
        dates[0], dates[1]
    )).data
    for date in dates:
        assert ','.join(
            [
                (
                    '("' if i == 0 else '"'
                ) + (
                    str(
                        int(d) - 1
                    ).zfill(2) if i == 1 else d
                ) + (
                    '")' if i == 2 else '"'
                ) for i, d in enumerate(
                    date.split('-')
                )
            ]
        ).encode('utf8') in resp

def test_loader_local_links(client):
    temps = [ 'static/' + l for l in [
        toMimic('.css', True),
        toMimic('.js', True)
        ]]
    resp = datepicker(
        app, local=temps
        ).loader()
    for t in temps:
        assert t in resp

def test_loader_local_links_win_false(client):
    try:
        datepicker(
            app, 
            local=['200', '200'],
            testing=True).loader()
    except Exception as e:
        assert type(e) == FileNotFoundError

def test_datepicker_false_input(client):
    try:
        datepicker(
            app=None
        )
    except Exception as e:
        assert type(e) == AttributeError
    try:
        datepicker(
            app=app,
            local=['200', '200', '200']
        ).loader()
    except Exception as e:
        assert type(e) == TypeError
    try:
        datepicker(
            app=app
        ).loader(theme='200')
    except Exception as e:
        assert type(e) == TypeError
    try:
        datepicker(
            app=app
        ).picker(id=200)
    except Exception as e:
        assert type(e) == TypeError

if __name__ == '__main__':
    app.run(port=8080, debug=False)