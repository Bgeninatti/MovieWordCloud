import setuptools
from mwc import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mwc-pkg-BGENINATTI",
    version=__version__,
    author="Bruno Geninatti",
    author_email="brunogeninatti@gmail.com",
    description="A bot that tweets wordclouds based on movies scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bgeninatti/MovieWordCloud",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'srt==3.0.0',
        'wordcloud==1.8.1',
        'requests==2.27.0',
        'peewee==3.13.1',
        'click==8.0.3',
        'tweepy==4.10.0',
        'attrs==21.4.0',
        'psycopg2',
        'dropbox==11.32.0',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'mwc=mwc.cli.cli:main',
        ],
    },
)
