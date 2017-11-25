"""
Flask-Formspree
-------------

A Flask extension to add Jquery-UI javascript date picker into the template,
it makes adding and configuring multiple date pickers at a time much easier
and less time consuming

"""
from setuptools import setup


setup(
    name='Flask-Datepicker',
    version='0.1',
    url='https://github.com/mrf345/flask_datepicker/',
    download_url='https://github.com/mrf345/flask_datepicker/archive/0.1.tar.gz',
    license='MIT',
    author='Mohamed Feddad',
    author_email='mrf345@gmail.com',
    description='date picker flask extension',
    long_description=__doc__,
    py_modules=['datepicker'],
    packages=['flask_datepicker'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-Bootstrap'
    ],
    keywords=['flask', 'extension', 'date', 'picker', 'jquery-ui',
              'datepicker'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
