#!/usr/bin/env-python
# -*- coding: utf-8 -*-

#   This work is licensed under a Creative Commons
#   Attribution 1.0 License.

import setuptools

setuptools.setup(
    name="rollnjump",
    version="2.0.0",
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': [
        'rollnjump=rollnjump.main:main'
    ]},
    include_package_data=True,
    package_data={"rollnjump": ["assets/font/*",
                                "assets/music/*",
                                "assets/img/*",
                                "assets/img/ui/*",
                                "assets/img/ui/fr/*",
                                "assets/img/ui/en/*",
                                "assets/img/ui/flag/*",
                                "assets/img/cloud/*",
                                "assets/img/item/*",
                                "assets/img/mono/*",
                                "assets/img/monogreen/*",
                                "assets/img/monopurple/*",
                                "assets/img/monored/*",
                                "assets/img/monowhite/*",
                                "assets/img/tree/*",
                                "modules/*",
                                "*.py"]},
    install_requires=['pygame>=2.0.0']
)
