#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#
# @name   : Infoga - Email OSINT
# @url    : http://github.com/m4ll0k
# @author : Momo Outaadi (m4ll0k)

from setuptools import setup 

setup(
    name='infoga',

    version='0.1.5',
    description='Email OSINT',
    url='https://github.com/m4ll0k',
    
    author = 'Momo (m4ll0k) Outaadi',
    author_email='m4ll0k@protonmail.com',
    license='GPLv3',

    install_requires = ['colorama','requests','urllib3'],
    console =['infoga.py'],
)