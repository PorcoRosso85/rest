import subprocess

import pytest


def rncmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output


def test_gh_workflow_list():
    output = rncmd("gh workflow list")
    print(f"\n### output: {output}")
    assert b"active" in output


@pytest.mark.skip
def test_gh_workflow_enable():
    output = rncmd("gh workflow enable")
    print(f"\n### output: {output}")
    assert b"there are no disabled" in output
