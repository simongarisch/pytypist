from setuptools import setup, find_packages


with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    author="Simon Garisch",
    author_email="gatman946@gmail.com",
    description="A typing tutor built with PyQt.",
    install_requires=["PyQt5==5.10.1"],
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="pytypist",
    name="pytypist",
    packages=find_packages(include=["pytypist"]),
    test_suite="tests",
    url="https://github.com/simongarisch/pytypist",
    version="0.1.0",
)