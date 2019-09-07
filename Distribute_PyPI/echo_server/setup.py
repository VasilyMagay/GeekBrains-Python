import setuptools

setuptools.setup(
    name='echo_server',
    version='1.0.0.0',
    author='Vasily Magay',
    author_email='org6cfpcsjk7@mail.ru',
    description='Echo server template',
    url='',
    packages=["src"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)

# Варианты для поля classifiers по ссылке: https://pypi.org/classifiers/

# pip install setuptools, wheel, twine
# python setup.py sdist bdist_wheel
# python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
