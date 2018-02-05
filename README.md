<h1 align='center'> flask_datepicker </h1>
<h3 align='center'>A Flask extension for Jquery-ui date picker, it makes adding and customizing multiple date pickers simpler and less time consuming.</h3>

## Install it :
#### - With pip
`pip install Flask-Datepicker` <br />
#### - or from github
`git clone https://github.com/mrf345/flask_datepicker.git`<br />
`cd flask_datepicker` <br />
`python setup.py install`
## Run it :
```python
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker

app = Flask(__name__)
Bootstrap(app)
datepicker(app)
```
#### inside the template

```jinja

{% extends 'bootstrap/base.html' %}
{% block scripts %}
  {{ super() }}
  {{ datepicker.loader() }}
  {{ datepicker.picker(id=".dp") }}
{% endblock %}
{% block content %}
  <form class="verticalform">
    <input type="text" class="form-control dp" />
  </form>
{% endblock %}

```
#### _Result_
![Datepicker](https://raw.githubusercontent.com/usb-resetter/usb-resetter.github.io/master/images/datepicker.png)

## Settings:
#### - Local Jquery-ui
##### by default the extension will load Jquery-ui plugin from [a remote CDN][25530337]. Although you can configure that to be locally through passing a list of two files .js and .css into the datepicker module like such:
```python
datepicker(app=app, local=['static/js/jquery-ui.js', 'static/css/jquery-ui.css'])
```
##### _The order in-which the items of list are passed is not of importance, it will be auto detected via file extension_

[25530337]: https://code.jquery.com/ui/ "Jquery-ui CDN"

#### - Customize datepicker
##### - Themes
##### datepicker.loader() allows you to select a specific theme of your choice via:
```python
datepicker.loader(theme="base")
```
##### _Or let it chose randomly_
```python
datepicker.loader(random_theme=True)
```
##### _This will chose new random theme with each reload of the page. To make it remember the random choice, use instead_
```python
datepicker.loader(random_remember=True)
```
##### _List of available themes :_
`
['base', 'black-tie', 'blitzer' 'cupertino','dark-hive', 'dot-luv', 'eggplant', 'excite-bike', 'flick', 'hot-sneaks', 'humanity', 'le-frog','mint-choc', 'overcast', 'pepper-grinder', 'redmond','smoothness', 'south-street', 'start', 'sunny','swanky-purse', 'trontastic', 'ui-darkness','ui-lightness', 'vader']
`

##### - dates settings:
##### The accepted arguments to be passed to the `datepicker.picker()` function are as follow:
```python
def picker(self, id=".datepicker", # identifier will be passed to Jquery to select element
                  dateFormat='yy-mm-dd', # can't be explained more !
                  maxDate='2018-12-30', # maximum date to select from. Make sure to follow the same format yy-mm-dd
                  minDate='2017-12-01'): # minimum date
```

## Credit:
> - [Datepicker][1311353e]: jQuery-ui date picker.

  [1311353e]: https://jqueryui.com/datepicker/ "jQuery-UI website"
