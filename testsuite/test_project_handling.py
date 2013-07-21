from __future__ import print_function

from plumbum import local
import pytest

from loslassa.loslassa import LoslassaProject, LoslassaStart
from loslassa.utils import *
from conftest import assert_exc_contains


class TestLoslassaProject(object):
    def test_empty_path_raises_error(self):
        with pytest.raises(AssertionError):
            LoslassaProject(None)

    @pytest.mark.usefixtures("work_in_empty_tmpdir")
    def test_normal_project(self):
        lp = LoslassaProject("test")
        lp.create_project()
        assert lp.sphinxConfig.exists()
        assert lp.isProject


class TestLoslassaStart(object):
    @pytest.mark.usefixtures("work_in_empty_tmpdir")
    def test_start_in_existing_dir_raises(self):
        ls = LoslassaStart("dummy_executable")
        ls.projectPath = local.cwd
        with assert_exc_contains(LoslassaError, "already exists"):
            ls.main()

    @pytest.mark.usefixtures("work_in_empty_tmpdir")
    def test_start_without_name_raises(self):
        ls = LoslassaStart("dummy_executable")
        with assert_exc_contains(LoslassaError, "provide a name"):
            ls.main()

    @pytest.mark.usefixtures("work_in_empty_tmpdir")
    def test_start_with_good_name_creates_project(self):
        ls = LoslassaStart("dummy_executable")
        ls.projectPath = local.cwd/"new_project"
        ls.main()
        assert ls.project.projectName == "new_project"
