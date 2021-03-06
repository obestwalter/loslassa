from __future__ import print_function
from contextlib import contextmanager

from plumbum.machines.local import local
import pytest

from loslassa._loslassa import LoslassaProject


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
        root = path / name
        dummyProject = LoslassaProject(root)
        dummyProject.create_project()
    return projectPaths


# noinspection PyUnusedLocal
@pytest.fixture
def work_in_dummy_project(work_in_empty_tmpdir):
    return create_dummy_projects(local.cwd)


@contextmanager
def assert_exc_contains(exc, content):
    """check if exception of type `exc` is raised with content

    :param exc: Exception type
    :param content: content that should be part of the exception message
    :type content: str or list
    """
    try:
        yield
    except Exception as e:
        assert type(e) == exc
        message = e.args[0]  # warning might not always work
        if isinstance(content, str):
            assert content in message
        else:
            assert all(m in message for m in content)
    else:
        raise Exception("Did not raise %s with %s" % (exc, content))


def chdir_in_and_out(request, path):
    """change into path and change back on exit"""
    oldWorkDirStr = str(local.cwd)
    workDir = local.cwd
    workDir.chdir(path)
    request.addfinalizer(lambda: workDir.chdir(oldWorkDirStr))
    return type("", (), {"oldWorkDirStr": oldWorkDirStr})
