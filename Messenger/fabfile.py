from fabric.api import local
import subprocess
import platform


def server():
    local('python server')


def migrate():
    local('python server -m')


def client():
    local('python client')


def test():
    local('pytest --cov-report term-missing --cov server')


def notebook():
    local('jupiter notebook')


def kill():
    local('lsof -t -i tcp:8000 | xarg kill')


def clients(num):
    windows = platform.system().lower() == 'windows'
    for i in range(int(num)):
        if windows:
            proc = subprocess.Popen('python client', creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            proc = subprocess.Popen('python client', shell=True)


def client_admin():
    local('python client -a')


def apidoc():
    local('sphinx-apidoc -o docs/source server')
