from __future__ import print_function

from plumbum.local_machine import LocalPath
import pytest

from conftest import params
from loslassa.loslassa import LoslassaProject
from loslassa.utils import find_file, UtilsError
from testsuite.conftest import generate_dummy_projects


@pytest.mark.usefixtures("work_in_empty_tmpdir")
@params([dict(path="."), dict(path=LocalPath("."))])
def test_different_path_types(path):
    with pytest.raises(UtilsError) as excInfo:
        find_file(path, "dontcare")
    assert "not found" in excInfo.exconly()


@pytest.mark.usefixtures("work_in_example_project")
def test_conf_file_found_in_example_project():
    foundFile = find_file(".", LoslassaProject.CONF_FILE_NAME)
    assert foundFile.basename == LoslassaProject.CONF_FILE_NAME


def test_conf_file_not_found_raises(tmpdir):
    wantedFileName = LoslassaProject.CONF_FILE_NAME
    with pytest.raises(UtilsError) as excInfo:
        find_file(tmpdir, wantedFileName)
    assert "not found" in excInfo.exconly()


def test_too_many_conf_files_found_raises(tmpdir):
    tmpdir = LocalPath(tmpdir)
    generate_dummy_projects(tmpdir, 2)
    with pytest.raises(UtilsError) as excInfo:
        find_file(tmpdir, LoslassaProject.CONF_FILE_NAME)
    assert "too many" in excInfo.exconly()
