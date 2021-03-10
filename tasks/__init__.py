from invoke import Collection
from rich import pretty, traceback

from . import local

pretty.install()
traceback.install()

ns = Collection.from_module(local)