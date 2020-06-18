import atexit as at_exit
import os
from random import randint
from shutil import rmtree


base_dir = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(base_dir, 'templates')
static = os.path.join(base_dir, 'static')
directories = [templates, static]


for d in directories:
    if not os.path.isdir(d):
        os.mkdir(d)


def mock_template(content):
    template_name = None
    template_path = None

    while not template_name:
        temp_name = '%i.html' % randint(1, 10000)
        template_path = os.path.join(templates, temp_name)

        if not os.path.isfile(template_path):
            template_name = temp_name

    with open(template_path, 'w+') as template:
        template.write(content)

    return temp_name


def mock_static(extension, content='Emptiness'):
    static_name = None
    static_path = None

    while not static_name:
        temp_name = '%i.%s' % (randint(1, 10000), extension)
        static_path = os.path.join(static, temp_name)

        if not os.path.isfile(static_path):
            static_name = temp_name

    with open(static_path, 'w+') as static_file:
        static_file.write(content)

    return 'static/%s' % static_name


def teardown():
    for d in directories:
        if os.path.isdir(d):
            rmtree(d)


at_exit.register(teardown)
