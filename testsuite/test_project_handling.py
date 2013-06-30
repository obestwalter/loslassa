from plumbum import LocalPath
import pytest

from loslassa.loslassa import LoslassaProject
from loslassa.utils import LoslassaError


class TestLoslassaProject(object):
    def test_empty_path_raises_error(self):
        with pytest.raises(LoslassaError):
            LoslassaProject(None)

    def test_project_paths_are_initialized(self):
        lp = LoslassaProject(".")
        assert len(lp.allPaths) > 0
        for p in lp.allPaths:
            assert type(p) == LocalPath
