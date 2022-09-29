import setuptools

from sunflower import __version__

setuptools.setup(
    name="sunflower",
    version=__version__,
    packages=setuptools.find_packages(),
    install_requires=(
        "selenium>=3.141.0",
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
        "peewee>=3.14.4",
        "click>=8.0.1",
        "python-decouple>=3.4"
        "requests-cache>=0.7.2"
    ),
    entry_points={
        "console_scripts": ["sunflower=sunflower.cli.core:main"]
    },
)
