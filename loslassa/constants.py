import os


__all__ = [
    'SOURCE_PATH',
    'BUILD_DIR',
    'DOCTREES_PATH',
    'LOSLASSA_ROOT',
    'OUTPUT_PATH',
    'PROJECT_ROOT',
    'EXAMPLE_PROJECT_PATH',
]

LOSLASSA_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(LOSLASSA_ROOT, ".."))
BUILD_DIR = "build"
EXAMPLE_PROJECT_PATH = os.path.join(PROJECT_ROOT, "example_project")
DOCTREES_PATH = os.path.join(EXAMPLE_PROJECT_PATH, BUILD_DIR, "doctrees")
OUTPUT_PATH = os.path.join(EXAMPLE_PROJECT_PATH, BUILD_DIR, "html")
SOURCE_PATH = os.path.join(EXAMPLE_PROJECT_PATH, "source")
