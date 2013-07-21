from __future__ import print_function
from contextlib import contextmanager

from plumbum import local
import pytest

from loslassa.loslassa import LoslassaProject


@pytest.fixture
def work_in_example_project(request):
    """Change into example project and back on exit"""
    return chdir_in_and_out(request, LoslassaProject.EXAMPLE_PROJECT)


@pytest.fixture
def work_in_empty_tmpdir(request, tmpdir):
    """Change into empty tmpdir and back on exit"""
    return chdir_in_and_out(request, tmpdir)


def create_dummy_projects(path, numProjects=1):
    """create minimal projects with generic names

    :returns: paths of the created projects
    """
    assert path.exists()
    with pytest.raises(StopIteration):
        next(path.walk())
    projectPaths = []
    for idx in range(numProjects):
        name = "dummy_project_%s" % (idx)
        root = path/name
        dummyProject = LoslassaProject(root)
        dummyProject.create_project()
    return projectPaths


@contextmanager
def assert_exc_contains(exc, content):
    """check if exception of type `exc` is raised with content

    :param Exception exc: Exception type
    :param content: content that should be part of the exception message
    :type content: basestring or list of basestring
    """
    try:
        yield
    except Exception as e:
        assert type(e) == exc
        if isinstance(content, basestring):
            assert content in e.message
        else:
            assert all(m in e.message for m in content)


def chdir_in_and_out(request, path):
    """change into path and change back on exit"""
    oldWorkDirStr = str(local.cwd)
    workDir = local.cwd
    workDir.chdir(path)
    request.addfinalizer(lambda: workDir.chdir(oldWorkDirStr))
    return type("", (), {"oldWorkDirStr": oldWorkDirStr})
