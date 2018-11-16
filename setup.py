import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AutoSite",
    version="1.0.5",
    author="dotcomboom",
    author_email="dotcomboom@protonmail.com",
    description="Keep all your website's pages under one template",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dotcomboom/AutoSite",
    packages=setuptools.find_packages(),
    install_requires=[
        'pathlib',
        'bs4',
        'markdown',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Markup :: HTML"
    ],
    entry_points={
          'console_scripts': ['autosite=AutoSite.__init__:main'],
    },
)
