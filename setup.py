#!/usr/bin/env-python
# -*- coding: utf-8 -*-
# pylint: disable-all

# Roll 'n' Jump
# Written in 2020, 2021 by Samuel Arsac, Hugo Buscemi,
# Matteo Chencerel, Rida Lali
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

import setuptools

setuptools.setup(
    name="rollnjump",
    version="2.0.0",
    licence="CC0 1.0",
    classifiers=[
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Libraries :: pygame'
    ],
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
