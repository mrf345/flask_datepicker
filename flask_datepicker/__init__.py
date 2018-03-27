from flask import Markup
from os import path, name as osName
from random import choice
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class datepicker(object):
    def __init__(self, app=None, local=[]):
        """
        Initiating the extension and seting up important varibles
        @param: app flask application instance (default None).
        @param: local contains Jquery UI local sourcecode files (default [])
        """
        self.app = app
        self.local = local
        self.random_theme = None  # to change if recieved random_theme=True
        if self.app is not None:
            self.init_app(app)
        else:
            # throwing error for not recieving app
            raise(AttributeError("must pass app to datepicker(app=)"))
        if self.local != []:
            # cheacking the length of the recieved list and throwing error
            if len(self.local) != 2:
                raise(
                    TypeError(
                        "datepicker(local=) requires a list of" +
                        " two files jquery-ui.js and jquery-ui.css"))
        self.injectem()  # resposible of injecting modals into the template

    def init_app(self, app):
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def teardown(self, exception):
        pass

    def injectem(self):
        """ datepicker injecting itself into the template as datepicker """
        @self.app.context_processor
        def inject_vars():
            return dict(datepicker=self)

    def loader(self, theme=None, random_theme=False, random_remember=True):
        """
        Function that allows customizing Jquery UI upon loading it
        @param: theme it takes string of Jquery UI theme name (default None).
        @param: random_theme to allow the extension to choose a random theme
        for Jquery UI (default True).
        @param: random_remember to remember the random choice, unless you want
        it to load new theme with each reload (default True).
        """
        html = ""  # html tags will end-up here
        for i, n in enumerate(('js', 'css')):
            if self.local == []:
                themes = ('base', 'black-tie', 'blitzer' 'cupertino',
                          'dark-hive', 'dot-luv', 'eggplant', 'excite-bike',
                          'flick', 'hot-sneaks', 'humanity', 'le-frog',
                          'mint-choc', 'overcast', 'pepper-grinder', 'redmond',
                          'smoothness', 'south-street', 'start', 'sunny',
                          'swanky-purse', 'trontastic', 'ui-darkness',
                          'ui-lightness', 'vader')  # Jquery UI offical themes
                if theme is not None and not random_theme:
                    if theme not in themes:
                        raise(
                            TypeError(
                                "datepicker.picker(theme=) must be one" +
                                " of jquery-ui offical themes"))
                theme = choice(themes) if (random_theme or
                                           random_remember and
                                           self.random_theme is None
                                           ) else self.random_theme
                # choosing randomly, if conditions allow, otherwise if not
                links = ['https://code.jquery.com/ui/1.12.1/themes/' +
                         '%s/jquery-ui.css' % theme,
                         'https://code.jquery.com/ui/1.12.1/jquery-ui.min.js']
            else:
                links = self.local
                def togglePath(rev=False, links=links):
                    """
                        Function to fix windows OS relative path issue
                        ISSUE 1 : windows os path
                        if windows used and windows path not used.
                    """
                    if osName == 'nt':
                        order = ['/', '\\']
                        if rev:
                            order.reverse()
                        for linkIndex, link in enumerate(links):
                            links[linkIndex] = link.replace(order[0], order[1])
                
                togglePath(False)
                # checking if Jquery UI files exist
                if not path.isfile(links[0]) and not path.isfile(links[1]):
                    raise(FileNotFoundError(
                        "datepicker.loader() file not found "))
                togglePath(True)
            tags = ['<script src="%s"></script>\n',
                    '<link href="%s" rel="stylesheet">\n']
            html += tags[i] % [  # didn't know that .endwith() was a thing
                l for l in links if l.split(  # stiil like it more this way
                    '.')[len(l.split('.')) - 1] == n][0]
        return Markup(html)  # making sure html safe

    def picker(self, id=".datepicker",
               dateFormat='yy-mm-dd',
               maxDate='',
               minDate=''):
        """
        datepicker initilizer, it produces a javascript code to load the plugin
        witn passed arguements
        @param: id the identifier which jquery will assign datapickers to
        (default '.datepicker').
        @param: dateFormat the format of a date ! (default 'yy-mm-dd').
        @param: maxDate Example:2017-12-30 the maximum selectable date
        (default '').
        @param: minDate Example:2016-01-01 the minimum selectable date
        (default: '').
        """
        for h, a in {'id': id,
                     'dateFormat': dateFormat,
                     'maxDate': maxDate,
                     'minDate': minDate}.items():
            if not isinstance(a, str):
                raise(TypeError("datepicker.picker(%s) takes string" % h))
        date_limits = []
        # trying to iterate with fail safe, without any more raises
        for s in [maxDate, minDate]:
            ss = s.split('-') if len(s.split('-')) == 3 else []
            ss = 'new Date("%s","%s","%s")' % (ss[0],
                                               ss[1],
                                               ss[2]) if ss != [] else "null"
            date_limits.append(ss)
        return Markup(" ".join(['<script>',
                                '$(document).ready(function() {'
                                '$("%s").datepicker({' % id,
                                'dateFormat: "%s",' % dateFormat,
                                'maxDate: %s,' % date_limits[0],
                                'minDate: %s' % date_limits[1],
                                '});})', '</script>']))
