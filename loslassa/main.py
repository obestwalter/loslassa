#!/usr/bin/env python
import logging
import os
import sys

# noinspection PyUnresolvedReferences
from plumbum.cmd import sphinx_build

# quick hack to make this work without adding something to PYTHONPATH
path = os.path.dirname(os.path.abspath(__file__)).rpartition('loslassa')[0]
if path not in sys.path:
    sys.path.insert(0, path)

from loslassa.constants import *
from loslassa.devserver import serve_with_reloader

log = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    htmlBuilder = sphinx_build[
        "-b", "dirhtml", "-d", DOCTREES_PATH, SOURCE_PATH, OUTPUT_PATH]

    serve_with_reloader(OUTPUT_PATH, 8080, htmlBuilder,pathToWatch=SOURCE_PATH)
