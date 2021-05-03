from setuptools import setup, find_packages

exec(open("apisla/_version.py", encoding="utf-8").read())

LONG_DESC = open("README.rst", encoding="utf-8").read()

setup(
    name="apisla",
    version=__version__,
    description="SLAs for APIs managing load & performance guarantees.",
    url="https://actorforth.org",
    long_description=LONG_DESC,
    author="Benjamin Scherrey",
    author_email="scherrey@actorforth.org",
    license="<COOKIECUTTER-TRIO-TODO: fill me in!>",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["trio", "trio-typing"],
    keywords=[
        # COOKIECUTTER-TRIO-TODO: add some keywords
        # "async", "io", "networking", ...
    ],
    python_requires=">=3.8",
    classifiers=[
        "Framework :: Trio",
        # COOKIECUTTER-TRIO-TODO: Remove any of these classifiers that don't
        # apply:
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        # COOKIECUTTER-TRIO-TODO: Consider adding trove classifiers for:
        #
        # - Development Status
        # - Intended Audience
        # - Topic
        #
        # For the full list of options, see:
        #   https://pypi.org/classifiers/
    ],
)
