from flask import Flask, render_template
# from flask_datepicker import datepicker
# Some junk to solve loading module path from parent dir
import sys
import os
spliter = '\\' if os.name == 'nt' else '/'
sys.path.append(
    spliter.join(
        os.getcwd().split(
            spliter
        )[:-1]
    )
)
# End of junk
from flask_datepicker import datepicker

app = Flask(__name__, template_folder='.')
datepicker(app, local=['static/jquery-ui.min.js', 'static/jquery-ui.min.css'])


@app.route('/')
def root():
    return render_template('index.html')


app.run(debug=True, port=4000)
