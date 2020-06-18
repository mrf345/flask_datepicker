import os


THEMES = ['base', 'black-tie', 'blitzer' 'cupertino',
          'dark-hive', 'dot-luv', 'eggplant', 'excite-bike',
          'flick', 'hot-sneaks', 'humanity', 'le-frog',
          'mint-choc', 'overcast', 'pepper-grinder', 'redmond',
          'smoothness', 'south-street', 'start', 'sunny',
          'swanky-purse', 'trontastic', 'ui-darkness',
          'ui-lightness', 'vader']

JS_REMOTE = 'https://code.jquery.com/ui/%s/jquery-ui.min.js'
CSS_REMOTE = 'https://code.jquery.com/ui/%s/themes/%s/jquery-ui.css'

WINDOWS = os.name == 'nt'
