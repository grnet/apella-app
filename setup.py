import distutils.log
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as _build_py
import os
import subprocess

with open("version.txt") as f:
    PACKAGE_NAME, VERSION, COMPATIBLE_VERSION = \
        (x.strip() for x in f.read().strip().split())

with open('requirements.txt') as f:
    INSTALL_REQUIRES = [
        x.strip('\n')
        for x in f.readlines()
        if x and x[0] != '#'
    ]

SHORT_DESCRIPTION = "Election of Faculty members"

PACKAGES_ROOT = '.'
PACKAGES = find_packages(PACKAGES_ROOT)

# Package meta
CLASSIFIERS = []

EXTRAS_REQUIRES = {
}

TESTS_REQUIRES = [
]


def get_all_data_files(dest_path, source_path):
    dest_path = dest_path.strip('/')
    source_path = source_path.strip('/')
    source_len = len(source_path)
    return [
        (
            os.path.join(dest_path, path[source_len:].strip('/')),
            [os.path.join(path, f) for f in files],
        )
        for path, _, files in os.walk(source_path)
    ]


UI_DATA_FILES = get_all_data_files('lib/apella/resources/www/ui', 'ui/dist')

APELLA_TEMPLATE_FILES = get_all_data_files(
        'lib/apella/resources/templates',
        'apella/templates')

MIGRATION_QUERY_FILES = get_all_data_files(
    'lib/apella/resources/migration_queries',
    'resources/migration_queries')


class BuildUiCommand(_build_py):
    """ Extend build_py to build Apella UI. """

    description = 'build Apella UI'
    user_options = _build_py.user_options + [
        ('no-ui', None, 'skip Apella UI build'),
    ]

    boolean_options = _build_py.boolean_options + ['no-ui']

    def initialize_options(self):
        """ Set default values for options. """

        _build_py.initialize_options(self)
        self.no_ui = None

    def run(self):
      if not self.no_ui:
        command = ['./build_ui.sh', 'production']
        self.announce('building ui: %s' % ' '.join(command),
                      level=distutils.log.INFO)
        subprocess.call(command, cwd='./ui/')

      _build_py.run(self)


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    license='GPLv3',
    description=SHORT_DESCRIPTION,
    classifiers=CLASSIFIERS,
    packages=PACKAGES,
    package_dir={'': PACKAGES_ROOT},
    data_files=[
        ('lib/apella/resources', ['resources/common.json',
                                  'resources/holidays.json',
                                  'resources/apella.apimas',
                                  'resources/schools.csv',
                                  'resources/subject_areas_subjects.csv',
                                  'resources/institutions.csv',
                                  'resources/departments.csv']),
        ('lib/apella/scripts', ['scripts/apella_init.sh']),
    ] + UI_DATA_FILES + MIGRATION_QUERY_FILES + APELLA_TEMPLATE_FILES,
    zip_safe=False,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRES,
    tests_require=TESTS_REQUIRES,

    entry_points={
        'console_scripts': [
            'apella = apella.management:main',
        ],
    },
    cmdclass={'build_py': BuildUiCommand},
)
