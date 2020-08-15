import os
from flask import Markup, url_for
from random import choice

from flask_datepicker.constants import THEMES, JS_REMOTE, CSS_REMOTE, WINDOWS
from flask_datepicker.utils import find, cache_output


class datepicker(object):
    def __init__(self, app=None, local=[], version='1.12.1'):
        '''Extension to help with loading and using jQueryUI Datepicker.

        Parameters
        ----------
        app : Flask, optional
            Flask application instance, by default None
        local : list, optional
            list of jQuery UI local files as relative paths, by default []
        version : str, optional
            jQuery UI version to fetch remotely, by default '1.12.1'
        '''
        self.__app = app
        self.__local = local
        self.__random_theme = choice(THEMES)
        self.__version = version

        self.__app and self.__inject()

    def init_app(self, app):
        '''Lazy load Flask application.

        Parameters
        ----------
        app : Flask App Instance
        '''
        self.__app = app
        self.__inject()

    def __inject(self):
        '''Injecting `datapicker` instance into the template.'''
        @self.__app.context_processor
        def _inject_vars():
            return dict(datepicker=self)

    @cache_output
    def __resolve_local(self, absolute=False):
        '''Check if static folder is `self.__local` and resolve it.

        Returns
        -------
        str
            list of absolute paths to resolved `self.__local`
        '''
        folder = self.__app.static_folder
        folder_name = os.path.basename(folder)
        local = self.__local or []
        resolved_local = []

        for link in local:
            resolved_link = link

            if folder_name in resolved_link:
                resolved_link = resolved_link\
                    .replace('%s%s' % (folder_name, '\\'), '')\
                    .replace('%s%s' % (folder_name, '/'), '')
            if absolute and WINDOWS and '/' in resolved_link:
                resolved_link = resolved_link.replace('/', '\\')

            resolved_local.append(resolved_link)

        with self.__app.app_context():
            return [os.path.join(folder, link) for link in resolved_local]\
                if absolute else [url_for('static', filename=link)
                                  for link in resolved_local]

    @property
    def __resolved_local_abs(self):
        return self.__resolve_local(absolute=True)

    @property
    def __resolved_local_rel(self):
        return self.__resolve_local()

    def loader(self, theme=None, random_remember=False, version='1.12.1'):
        '''Load jQuery UI assets and customize them, if wanted.

        Parameters
        ----------
        theme : str, optional
            jQuery theme name checkout `datepicker.constants.py::THEMES`, by default None
        random_remember : bool, optional
            Remember the randomly chosen jQuery theme, by default False
        version : str, optional
            jQuery UI version to fetch remotely, by default '1.12.1'

        Returns
        -------
        str
            Safe HTML content to load jQuery UI assets.
        '''
        links = self.__local or []
        version = version or self.__version
        theme = theme or (self.__random_theme if random_remember else choice(THEMES))
        files_not_exist = not all(os.path.isfile(f) for f in self.__resolved_local_abs)
        links = [CSS_REMOTE % (version, theme), JS_REMOTE % version]\
            if files_not_exist or not links else self.__resolved_local_rel

        css = find(lambda link: link.endswith('.css'), links)
        js = find(lambda link: link.endswith('.js'), links)

        return Markup('\n'.join(['<link href="%s" rel="stylesheet">' % css,
                                 '<script src="%s"></script>' % js]))

    def picker(self, id='.datepicker', dateFormat='yy-mm-dd',
               maxDate='', minDate='', btnsId='.btnId'):
        '''Assign a datepicker to a specific HTML element.

        Parameters
        ----------
        id : str, optional
            HTML element css selector, by default '.datepicker'
        dateFormat : str, optional
            date string format, by default 'yy-mm-dd'
        maxDate : str, optional
            maximum date to allow selecting, by default ''
        minDate : str, optional
            minimum date to allow selecting, by default ''
        btnsId : str, optional
            additional css selector to toggle datepicker's visibility, by default '.btnId'

        Returns
        -------
        str
            Safe HTML content to initiate and assign a new datepicker.
        '''
        date_limits = []
        for d in [maxDate, minDate]:
            ss = d.split('-') if len(d.split('-')) == 3 else []
            date_limits.append('new Date("%s","%s","%s")' % (
                ss[0],
                str(int(ss[1]) - 1).zfill(2),
                ss[2]) if ss != [] else 'null')

        return Markup(' '.join(['<script>',
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
