from setuptools import setup, find_packages
import io

name = 'maury_bot'
description = 'discord bot with gpt3'

# Read in requirements
requirements = open("requirements.txt").readlines()
requirements = [r.strip() for r in requirements]

packages = find_packages()
print(packages)

setup(
    name=name,
    version="0.0.1",
    author="Evan McKinney",
    author_email="evmckinney9@gmail.com",
    python_requires=(">=3.9.2"),
    install_requires=requirements,
    description=description,
    packages=packages
)