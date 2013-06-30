from __future__ import print_function

from plumbum import local


class TestWorkDirRestoration(object):
    oldWorkDirStr = str(local.cwd)

    def test_dir_change(self, work_in_example_project):
        assert work_in_example_project.oldWorkDirStr == self.oldWorkDirStr
        assert local.cwd != self.oldWorkDirStr

    def test_restoration(self):
        assert self.oldWorkDirStr == local.cwd
