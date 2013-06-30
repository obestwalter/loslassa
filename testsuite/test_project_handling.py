from __future__ import print_function

from plumbum import LocalPath, local
import pytest

from loslassa.loslassa import LoslassaProject, LoslassaStart
from loslassa import utils
from conftest import assert_exc_contains


class TestLoslassaProject(object):
    def test_empty_path_raises_error(self):
        with pytest.raises(utils.LoslassaError):
            LoslassaProject(None)

    def test_project_paths_are_initialized(self):
        lp = LoslassaProject(".")
        assert len(lp.allPaths) > 0
        for p in lp.allPaths:
            assert type(p) == LocalPath

    @pytest.mark.usefixtures("work_in_example_project")
    def test_check_sanity_in_project_dir_is_ok(self):
        lp = LoslassaProject(".")
        lp.check_sanity()

    @pytest.mark.usefixtures("work_in_empty_tmpdir")
    def test_check_sanity_in_empty_dir_raises(self,):
        lp = LoslassaProject(".")
        with pytest.raises(utils.LoslassaError):
            lp.check_sanity()


class TestLoslassaStart(object):
    @pytest.mark.usefixtures("work_in_empty_tmpdir")
    def test_start_in_existing_dir_raises(self):
        ls = LoslassaStart("dummy_executable")
        ls.projectPath = local.cwd
        with pytest.raises(utils.LoslassaError) as excInfo:
            ls.main()
        assert "exists already" in excInfo.exconly()

    @pytest.mark.usefixtures("work_in_empty_tmpdir")
    def test_start_without_name_raises(self):
        ls = LoslassaStart("dummy_executable")
        with assert_exc_contains(utils.LoslassaError, "provide a name"):
            ls.main()
