from setuptools import setup, find_packages

# Package info
PACKAGE_NAME = "apella"
VERSION = "0.1"
SHORT_DESCRIPTION = "Election of Faculty members"

PACKAGES_ROOT = '.'
PACKAGES = find_packages(PACKAGES_ROOT)

# Package meta
CLASSIFIERS = []

# Dependencies declared at requirements.txt
INSTALL_REQUIRES = [
]

EXTRAS_REQUIRES = {
}

TESTS_REQUIRES = [
]

# Provided as an attribute, so you can append to these instead
# of replicating them:
standard_exclude = ["*.py", "*.pyc", "*$py.class", "*~", ".*", "*.bak"]
standard_exclude_directories = [
    ".*", "CVS", "_darcs", "./build", "./dist", "EGG-INFO", "*.egg-info",
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    license='GNU GPLv3',
    description=SHORT_DESCRIPTION,
    classifiers=CLASSIFIERS,
    packages=PACKAGES,
    package_dir={'': PACKAGES_ROOT},
    data_files=[
        ('resources/www', ['resources/www/common.json',
                           'resources/www/holidays.json']),
    ],
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
