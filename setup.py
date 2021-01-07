import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mwc-pkg-BGENINATTI",
    version="0.0.2",
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
        'wordcloud==1.6.0',
        'requests==2.22.0',
        'peewee==3.13.1',
        'IMDbPY==6.8',
        'lxml==4.6.2'
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'mwc=mwc.cli:main',
        ],
    },
)
