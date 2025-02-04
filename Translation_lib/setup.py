import os
from setuptools import setup, find_packages # type: ignore


setup(
    name="translation",
    version="0.1.0",
    packages=find_packages(),
    description="this a library used to translate cdecl generated English-like phrases to telugu",
    url="https://github.com/Raphael-08/Cdecl-telugu",
    install_requires=[
        "flask==2.2.3",
        "werkzeug>=2.2.2,<3.0",
        "google-transliteration-api",
        "requests",
        "gunicorn"
    ]
)
