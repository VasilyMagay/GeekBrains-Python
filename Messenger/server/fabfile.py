from fabric.api import local


def server():
    local('python __main__.py')


def migrate():
    local('python __main__.py -m')


def apidoc():
    local('sphinx-apidoc -o docs/source .')
