from flask import Markup
from static_parameters import (
    function_parameters, class_parameters
)
from os import path, name as osName
from random import choice
# Fixing file not found for py2
from sys import version_info
if version_info[0] == 2:
    FileNotFoundError = IOError

@class_parameters(function_parameters)
class datepicker(object):
    def __init__(self, app=None, local=[], testing=False):
        """
        Initiating the extension and seting up important variables
        @param: app flask application instance (default None).
        @param: local contains Jquery UI local sourcecode files (default [])
        ((testing:bool))
        """
        self.testing = testing
        self.app = app
        self.local = local
        self.random_theme = None  # to change if received random_theme=True
        if self.app is None:
            # throwing error for not receiving app
            raise(AttributeError("must pass app to datepicker(app=)"))
        if self.local != []:
            # checking the length of the received list and throwing error
            if len(self.local) != 2:
                raise(
                    TypeError(
                        "datepicker(local=) requires a list of" +
                        " two files jquery-ui.js and jquery-ui.css"))
        self.injectThem()  # responsible of injecting modals into the template
        self.themes = ('base', 'black-tie', 'blitzer' 'cupertino',
        'dark-hive', 'dot-luv', 'eggplant', 'excite-bike',
        'flick', 'hot-sneaks', 'humanity', 'le-frog',
        'mint-choc', 'overcast', 'pepper-grinder', 'redmond',
        'smoothness', 'south-street', 'start', 'sunny',
        'swanky-purse', 'trontastic', 'ui-darkness',
        'ui-lightness', 'vader')  # Jquery UI official themes

    def injectThem(self):
        """ datepicker injecting itself into the template as datepicker """
        @self.app.context_processor
        def inject_vars():
            return dict(datepicker=self)

    def loader(self, theme=None, random_remember=False):
        """
        Function that allows customizing Jquery UI upon loading it
        @param: theme it takes string of Jquery UI theme name (default None).
        for Jquery UI (default True).
        @param: random_remember to remember the random choice, unless you want
        it to load new theme with each reload (default True).
        """
        html = ""  # html tags will end-up here
        for i, n in enumerate(('js', 'css')):
            if self.local == []:
                # ISSUE 2: fix random theme selection
                if self.random_theme is None:
                    self.random_theme = choice(self.themes)
                if theme is None:
                    theme = self.random_theme if random_remember else choice(self.themes)
                else:
                    if theme not in self.themes:
                        raise(
                            TypeError(
                                "datepicker.picker(theme=) must be one" +
                                " of jquery-ui official themes"))
                # choosing randomly, if conditions allow, otherwise if not
                links = ['https://code.jquery.com/ui/1.12.1/themes/%s/jquery-ui.css' % theme,
                         'https://code.jquery.com/ui/1.12.1/jquery-ui.min.js']
            else:
                links = self.local

                def togglePath(rev=False, links=links):
                    """
                        Function to fix windows OS relative path issue
                        ISSUE 1 : windows os path
                        if windows used and windows path not used.
                    """
                    if osName == 'nt' or self.testing:
                        order = ['/', '\\']
                        if rev or self.testing:
                            order.reverse()
                        for linkIndex, link in enumerate(links):
                            links[linkIndex] = link.replace(order[0], order[1])

                togglePath(False)
                # checking if Jquery UI files exist
                if not path.isfile(links[0]) and not path.isfile(links[1]):
                    raise(FileNotFoundError(
                        "datepicker.loader() file not found "))
                togglePath(True)
            tags = [
                '<script src="%s"></script>\n',
                '<link href="%s" rel="stylesheet">\n'
                ] if self.local == [] else [
                '<script src="/%s"></script>\n',
                '<link href="/%s" rel="stylesheet">\n'
                ]
            html += tags[i] % [  # didn't know that .endwith() was a thing
                l for l in links if l.split(  # still like it more this way
                    '.')[len(l.split('.')) - 1] == n][0]
        return Markup(html)  # making sure html safe

    def picker(self, id=".datepicker",
               dateFormat='yy-mm-dd',
               maxDate='',
               minDate='',
               btnsId='.btnId'
               ):
        """
        datepicker initializer, it produces a javascript code to load the plugin
        with passed arguments
        @param: id the identifier which jquery will assign datapickers to
        (default '.datepicker').
        @param: dateFormat the format of a date ! (default 'yy-mm-dd').
        @param: maxDate Example:2017-12-30 the maximum selectable date
        (default '').
        @param: minDate Example:2016-01-01 the minimum selectable date
        (default: '').
        @param: btnsId id assigned to instigating buttons if needed 
        (default '.btnId')
        ((id:str))((dateFormat:str))((maxDate:str))((minDate:str))((btnsId:str))
        """
        date_limits = []
        # trying to iterate with fail safe, without any more raises
        for s in [maxDate, minDate]:
            ss = s.split('-') if len(s.split('-')) == 3 else []
            ss = 'new Date("%s","%s","%s")' % (ss[0],
                                               str(int(ss[1]) - 1).zfill(2),
                                               ss[2]) if ss != [] else "null"
            date_limits.append(ss)
        return Markup(" ".join(['<script>',
                                '$(document).ready(function() {',
                                'var EL = $("%s");' % btnsId,
                                '$("%s").each(function () {' % id,
                                'var toF = this; $(this).datepicker({',
                                'dateFormat: "%s",' % dateFormat,
                                'maxDate: %s,' % date_limits[0],
                                'minDate: %s});' % date_limits[1],
                                'if (EL.length > 0) { $(EL[0]).click(',
                                'function (ev) { ev.preventDefault();', 
                                '$(toF).focus() }); EL = EL.slice(1)',
                                '};});})', '</script>']))
