from setuptools import setup, find_packages
import os

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


setup(
    name=PACKAGE_NAME,
    provides=[PACKAGE_NAME + ' (' + COMPATIBLE_VERSION + ')'],
    version=VERSION,
    license='GPLv3',
    description=SHORT_DESCRIPTION,
    classifiers=CLASSIFIERS,
    packages=PACKAGES,
    package_dir={'': PACKAGES_ROOT},
    data_files=[
        ('lib/apella/resources', ['resources/common.json',
                                  'resources/holidays.json']),
    ] + UI_DATA_FILES,
    zip_safe=False,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRES,
    tests_require=TESTS_REQUIRES,

    entry_points={
        'console_scripts': [
            'apella = apella.management:main',
        ],
    },
)
