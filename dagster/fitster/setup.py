from setuptools import find_packages, setup

setup(
    name="fitster",
    packages=find_packages(exclude=["fitster_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
