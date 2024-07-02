import pytest

from .setup import app, extension
from .mockers import mock_static


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['STATIC_FOLDER'] = 'static'
    app.config['SERVER_NAME'] = 'localhost'
    client = app.test_client()
    yield client


def test_loader_template_links(client):
    content = client.get('/loader').data.decode('utf-8')

    assert 'jquery-ui.min.js' in content
    assert 'jquery-ui.css' in content


def test_picker_template_script(client):
    content = client.get('/picker').data.decode('utf-8')

    assert 'var toF = this; $(this).datepicker({' in content


def test_picker_min_max_dates(client):
    dates = ['2018-07-03', '2019-07-03']
    content = client.get('/min_max/%s/%s' % (dates[0], dates[1]))\
                    .data.decode('utf-8')

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
        ) in content


def test_loader_local_links(client):
    local_links = [mock_static('css'), mock_static('js')]
    extension._local = local_links
    extension._get_resolved_local.__dict__.clear()
    html = extension.loader()

    for link in local_links:
        assert link in html


def test_loader_local_links_win_false(client):
    with pytest.raises(Exception) as e:
        extension._local = ['200', '200']
        extension.loader()
        assert type(e) is globals().get('FileNotFoundError', IOError)
