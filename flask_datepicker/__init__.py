from flask import current_app, Markup
from os import path
from random import choice
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class datepicker(object):
    def __init__(self, app=None, local=[]):
        self.app = app
        self.local = local
        self.random_theme = None
        if self.app is not None:
            self.init_app(app)
        else:
            raise(AttributeError("must pass app to datepicker(app=)"))
        if self.local != []:
            if len(self.local) != 2:
                raise(
                    TypeError(
                        "datepicker(local=) requires a list of" +
                        " two files jquery-ui.js and jquery-ui.css"))
        self.injectem()

    def init_app(self, app):
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def teardown(self, exception):
        pass

    def injectem(self):
        @self.app.context_processor
        def inject_vars():
            return dict(datepicker=self)

    def loader(self, theme=None, random_theme=False, random_remember=True):
        html = ""
        for i, n in enumerate(['js', 'css']):
            if self.local == []:
                themes = ['base', 'black-tie', 'blitzer' 'cupertino',
                          'dark-hive', 'dot-luv', 'eggplant', 'excite-bike',
                          'flick', 'hot-sneaks', 'humanity', 'le-frog',
                          'mint-choc', 'overcast', 'pepper-grinder', 'redmond',
                          'smoothness', 'south-street', 'start', 'sunny',
                          'swanky-purse', 'trontastic', 'ui-darkness',
                          'ui-lightness', 'vader']
                if theme is not None and not random_theme:
                    if theme not in themes:
                        raise(
                            TypeError(
                                "datepicker.picker(theme=) must be one" +
                                " of jquery-ui offical themes"))
                if random_theme:
                    theme = choice(themes)
                    self.random_theme = theme
                elif random_remember:
                    if self.random_theme is None:
                        self.random_theme = choice(themes)
                    theme = self.random_theme
                links = ['https://code.jquery.com/ui/1.12.1/themes/%s' % theme +
                         '/jquery-ui.css',
                         'https://code.jquery.com/ui/1.12.1/jquery-ui.min.js']
            else:
                links = self.local
                if not path.isfile(links[0]) and not path.isfile(links[1]):
                    raise(FileNotFoundError(
                        "datepicker.loader() file not found "))
            tags = ['<script src="%s"></script>\n',
                    '<link href="%s" rel="stylesheet">\n']
            html += tags[i] % [
                l for l in links if l.split(
                    '.')[len(l.split('.')) - 1] == n][0]
        return Markup(html)

    def picker(self, id=".datepicker",
               defaultDate='',
               dateFormat='yy-mm-dd',
               maxDate='',
               minDate=''):
        for h, a in {'id': id,
                     'defaultDate': defaultDate,
                     'dateFormat': dateFormat,
                     'maxDate': maxDate,
                     'minDate': minDate}.items():
            if not isinstance(a, str):
                raise(TypeError("datepicker.picker(%s) takes string" % h))
        return Markup(" ".join(['<script>',
                                '$("%s").datepicker({' % id,
                                'defaultDate: "%s",' % defaultDate,
                                'dateFormat: "%s",' % dateFormat,
                                'maxDate: "%s",' % maxDate,
                                'minDate: "%s"' % minDate,
                                '});', '</script>']))
