import pytest
from loslassa.loslassa import LoslassaProject, GitPorcelainPorcelain


class TestGitIntegration(object):
    @pytest.mark.usefixtures("work_in_empty_tmpdir")
    def test_local_repo(self):
        lp = LoslassaProject("test")
        lp.create_project()
        gpp = GitPorcelainPorcelain(lp.inputContainer)
        gpp.create_repo()
        assert gpp.isRepo

    @pytest.mark.usefixtures("work_in_empty_tmpdir")
    def test_ssh_seetings_project(self):
        lp = LoslassaProject("test")
        lp.create_project()
        gpp = GitPorcelainPorcelain(lp.inputContainer)
        assert gpp.sshUser == "user_here"
        assert gpp.remoteFqdn == "fqdn_here"
        assert gpp.privateKeyPath == "key_here"
