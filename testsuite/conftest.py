from __future__ import print_function

from plumbum import local
import pytest

from loslassa.loslassa import LoslassaProject


@pytest.fixture
def work_in_example_project(request):
    """change into the example project folder"""
    oldWorkDirStr = str(local.cwd)
    workDir = local.cwd
    workDir.chdir(LoslassaProject.EXAMPLE_PROJECT_PATH)
    print("switched from", oldWorkDirStr, "to", workDir)
    request.addfinalizer(lambda: workDir.chdir(oldWorkDirStr))
    return type("", (), {"oldWorkDirStr": oldWorkDirStr})


@pytest.fixture
def work_in_empty_tmpdir(request, tmpdir):
    """change into an empty tmpdir"""
    oldWorkDirStr = str(local.cwd)
    workDir = local.cwd
    workDir.chdir(tmpdir)
    print("switched from", oldWorkDirStr, "to", workDir)
    request.addfinalizer(lambda: workDir.chdir(oldWorkDirStr))
    return type("", (), {"oldWorkDirStr": oldWorkDirStr})


def params(funcarglist):
    def wrapper(function):
        function.funcarglist = funcarglist
        return function

    return wrapper


def pytest_generate_tests(metafunc):
    for funcargs in getattr(metafunc.function, 'funcarglist', ()):
        metafunc.addcall(funcargs=funcargs)


def generate_dummy_projects(path, numProjects=1):
    assert path.exists()
    assert not list(path.walk())
    projectPaths = []
    for idx in range(numProjects):
        name = "dummy_project_%s" % (idx)
        root = path/name
        root.mkdir()
        dummyProject = LoslassaProject(root)
        for thisPath in dummyProject.neededDirPaths:
            thisPath.mkdir()
        for thisPath in dummyProject.neededFilePaths:
            thisPath.write("")
        dummyProject.check_sanity()
    return projectPaths
