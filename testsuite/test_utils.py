from __future__ import print_function
import logging

from plumbum.local_machine import LocalPath
import pytest

from loslassa.loslassa import LoslassaProject
from loslassa.utils import *
from conftest import *


class TestFindFile(object):
    @pytest.mark.usefixtures("work_in_example_project")
    def test_conf_file_found_in_example_project(self):
        foundFile = find_file(".", LoslassaProject.CONF_FILE_NAME)
        assert foundFile.basename == LoslassaProject.CONF_FILE_NAME

    @pytest.mark.usefixtures("work_in_empty_tmpdir")
    @pytest.mark.parametrize("path", (".", LocalPath(".")))
    def test_different_path_types_are_accepted(self, path):
        with assert_exc_contains(UtilsError, ["not found", "x"]):
            find_file(path, "x")

    def test_file_not_found_raises(self, tmpdir):
        with assert_exc_contains(UtilsError, ["not found", "x"]):
            find_file(tmpdir, "x")

    def test_too_many_files_found_raises(self, tmpdir):
        tmpdir = LocalPath(tmpdir)
        paths = create_dummy_projects(tmpdir, 3)
        with assert_exc_contains(UtilsError, ["too many"] + paths):
            find_file(tmpdir, LoslassaProject.CONF_FILE_NAME)


class TestAdjustLog(object):
    def test_bogus_level_raises(self):
        with assert_exc_contains(UtilsError, "unknown verbosity level"):
            adjust_log("bogus_level")

    def test_proper_level_adjust_level(self):
        adjust_log(logging.CRITICAL)
        log = logging.getLogger()
        assert log.getEffectiveLevel() == logging.CRITICAL
