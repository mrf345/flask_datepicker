from flask import Flask, render_template
from flask_datepicker import datepicker

from .mockers import mock_template

app = Flask(__name__)
eng = datepicker(app, local=[])


@app.route('/loader')
def loader():
    return render_template(mock_template("{{ datepicker.loader() }}"))


@app.route('/picker')
def picker():
    return render_template(mock_template("{{ datepicker.picker() }}"))


@app.route('/min_max/<min>/<max>')
def minMax(min, max):
    return render_template(
        mock_template(
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
