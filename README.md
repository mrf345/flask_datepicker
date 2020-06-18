<h1 align='center'> Flask-Datepicker </h1>
<p align='center'>
  <a href='https://travis-ci.com/mrf345/flask_datepicker'>
    <img src='https://travis-ci.com/mrf345/flask_datepicker.svg?branch=master' />
  </a>
  <a href='https://github.com/mrf345/flask_datepicker/releases'>
    <img src='https://img.shields.io/github/v/tag/mrf345/flask_datepicker' alt='Latest Release' />
  </a><br/>
  <a href='https://coveralls.io/github/mrf345/flask_datepicker?branch=master'>
    <img src='https://coveralls.io/repos/github/mrf345/flask_datepicker/badge.svg?branch=master' alt='Coverage Status' />
  </a>
  <a href='https://www.python.org/dev/peps/pep-0008/'>
    <img src='https://img.shields.io/badge/code%20style-PEP8-orange.svg' alt='Code Style' />
  </a>
  <a href='https://pypi.org/project/Flask-Datepicker/'>
    <img src='https://img.shields.io/pypi/dm/flask_datepicker' alt='Number of downloads' />
  </a>
</p>
<h3 align='center'>A Flask extension for jQueryUI DatePicker, it makes adding and customizing multiple date pickers simpler and less time consuming.</h3>

## Install:
#### - With pip
- `pip install Flask-Datepicker` <br />

#### - From the source:
- `git clone https://github.com/mrf345/flask_datepicker.git`<br />
- `cd flask_datepicker` <br />
- `python setup.py install`

## Setup:
#### - Inside Flask app:
```python
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker

app = Flask(__name__)
Bootstrap(app)
datepicker(app)
```

#### - Inside jinja template:
```jinja
{% extends 'bootstrap/base.html' %}
{% block scripts %}
  {{ super() }}
  {{ datepicker.loader() }} {# to load jQuery-ui #}
  {{ datepicker.picker(id=".dp") }}
{% endblock %}
{% block content %}
  <form class="verticalform">
    <input type="text" class="form-control dp" />
  </form>
{% endblock %}
```

## Settings:
#### - Options:
the accepted arguments to be passed to the `datepicker.picker()`:
```python
def picker(id=".datepicker", # identifier will be passed to Jquery to select element
           dateFormat='yy-mm-dd', # can't be explained more !
           maxDate='2018-12-30', # maximum date to select from. Make sure to follow the same format yy-mm-dd
           minDate='2017-12-01', # minimum date
           btnsId='.btnId' # id assigned to instigating buttons if needed
): 
```

##### - Themes
`datepicker.loader()` allows you to select a specific theme of your choice via:
```python
datepicker.loader(theme="base")
```

_If there is not a theme selected, the extension will select a new random theme with each reload of the page to be used. To make it remember the random choice, pass :_
```python
datepicker.loader(random_remember=True)
```

_List of available themes :_ <br />
`
['base', 'black-tie', 'blitzer' 'cupertino','dark-hive', 'dot-luv', 'eggplant', 'excite-bike', 'flick', 'hot-sneaks', 'humanity', 'le-frog','mint-choc', 'overcast', 'pepper-grinder', 'redmond','smoothness', 'south-street', 'start', 'sunny','swanky-purse', 'trontastic', 'ui-darkness','ui-lightness', 'vader']
`

#### - Local source:
by default the extension will load jQueryUI plugin from [a remote CDN][25530337]. Although you can configure that to be locally through passing a list of two files .js and .css into the datepicker module like such:
```python
datepicker(app=app, local=['static/js/jquery-ui.js', 'static/css/jquery-ui.css'])
```

[25530337]: https://code.jquery.com/ui/ "Jquery-ui CDN"

## Credit:
> - [Datepicker][1311353e]: jQuery-ui date picker.

  [1311353e]: https://jqueryui.com/datepicker/ "jQuery-UI website"
