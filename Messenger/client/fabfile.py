from fabric.api import local
import subprocess
import platform


def client():
    local('python __main__.py')


def client1():
    local('python __main__.py -c config1.yml')


def client2():
    local('python __main__.py -c config2.yml')


def clients(num):
    windows = platform.system().lower() == 'windows'
    for i in range(int(num)):
        if windows:
            proc = subprocess.Popen('python __main__.py', creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            proc = subprocess.Popen('python __main__.py', shell=True)


def apidoc():
    local('sphinx-apidoc -o docs/source .')


def register():
    local('python registration.py')
