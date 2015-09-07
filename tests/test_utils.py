import subprocess
from pytest import mark
from pytest_benchmark.utils import clonefunc, get_commit_info

f1 = lambda a: a


def f2(a):
    return a


@mark.parametrize('f', [f1, f2])
def test_clonefunc(f):
    assert clonefunc(f)(1) == f(1)
    assert clonefunc(f)(1) == f(1)


def test_clonefunc_not_function():
    assert clonefunc(1) == 1


@mark.parametrize('scm', ['git', 'hg'])
def test_get_commit_info(scm, testdir):
    subprocess.check_call([scm, 'init', '.'])
    testdir.makepyfile('asdf')
    subprocess.check_call([scm, 'add', 'test_get_commit_info.py'])
    subprocess.check_call([scm, 'commit', '-m', 'asdf'])
    out = get_commit_info()

    assert out.get('dirty') == False
    assert 'id' in out

    testdir.makepyfile('sadf')
    out = get_commit_info()

    assert out.get('dirty') == True
    assert 'id' in out