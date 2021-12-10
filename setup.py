"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['smartCart/views/welcomePageView.py']
DATA_FILES = ['smart-shopping-cart-1fbac-firebase-adminsdk-wfobd-09a600f28a.json','GFG.pdf']
OPTIONS = {'argv_emulation':True}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
