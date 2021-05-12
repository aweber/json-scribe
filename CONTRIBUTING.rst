How to contribute
=================
Thank you very much for reading this and taking the time to consider
contributing to and supporting Open Source software.  The really short
version is:

* set up a Python 3 development environment
* install the "dev" setuptools extra
* install the local package in editable mode
* run tests with "coverage run -m unittest discover tests"
* check style with flake8_ and yapf_
* fork the main repository and issue a pull request

If you don't understand any of that, then read on and *welcome to the
Open Source software community!*

.. _flake8: https://flake8.pycqa.org/en/latest/
.. _yapf: https://github.com/google/yapf

Set up a development environment
--------------------------------
You will want to have a virtual environment to do your development in.
**DO NOT sudo pip install!**  If you have a preferred environment
management tool, then here's what you need to know:

- use Python 3
- development toolchain is specified as the "dev" extra so you want
  the equivalent of ``pip install ".[dev]"``
- install the package in "editable" mode during development

If you aren't as well-versed in creating your own environment, then
read on.  I used the `venv Standard Library module`_ to create a new
virtual environment named *env* in the top-level directory::

   $ python3 -mvenv --upgrade-deps env

Next you need to install the development tools that this project uses::

   $ ./env/bin/pip install '.[dev]'

The development toolchain is included as an "extras_require" clause in
the package dependencies.  The last step is to install the package in
"editable mode"::

   $ ./env/bin/pip install -e .

At this point, you will have everything that you need to develop and test
the library installed into the local environment.

.. _venv Standard Library module: https://docs.python.org/3/library/venv.html

Run tests
---------
This project uses the `unittest Standard Library module`_ and Ned Batchelder's
excellent `coverage utility`_ to run tests.  You can use a different test
runner if you wish::

   $ ./env/bin/coverage run -m unittest discover tests
   .....................
   ----------------------------------------------------------------------
   Ran 21 tests in 0.003s

   OK
   $ ./env/bin/coverage report
   Name                       Stmts   Miss Branch BrPart  Cover   Missing
   ----------------------------------------------------------------------
   jsonscribe/__init__.py         5      0      2      0   100%
   jsonscribe/filters.py         16      0      4      0   100%
   jsonscribe/formatters.py      39      0     16      0   100%
   jsonscribe/utils.py           11      0      0      0   100%
   ----------------------------------------------------------------------
   TOTAL                         71      0     22      0   100%

I recommend running the tests **BEFORE** you start to change things.  This
practice will ensure that you are starting with a working environment.

.. _coverage utility: https://coverage.readthedocs.io/en/stable/
.. _unittest Standard Library module: https://docs.python.org/3/library/unittest.html

A word about code style
-----------------------
This project follows PEP-8 for style guidelines and uses yapf to ensure
that source code is formatted consistently.  If your contributions do not
match, then the pull request checks will fail.  Make sure that the following
two commands execute without failures::

   $ env/bin/flake8
   $ env/bin/yapf -dr jsonscribe tests

If there is no output, then your changes followed the style guide and you
are *good to go*.

Submit a pull request
---------------------
Before you create a pull request, there are a few more checks that you
should do.

* install and run tox_ to ensure language coverage
* build the documentation suite
* build source and wheel distributions

The continuous integration pipeline will do this when you create a new
pull request.  Run the following commands to make sure that your pull
request will pass the pipeline checks::

   $ env/bin/pip install -q tox wheel twine
   $ env/bin/tox -p auto
   $ env/bin/python setup.py sdist bdist_wheel
   $ env/bin/twine check dist/*
   $ env/bin/python setup.py build_sphinx

The twine checks will issue warnings about the lack of a
"long_description_content_type", this is fine and please do not fix it.
If any of the steps fail, then fix them (if you can) before you submit a
pull request.  If you run into problems that you cannot fix, submit the
pull request and ask for help.

If you haven't created a fork of the repository to contribute from, then
create a fork::

   https://github.com/aweber/json-scribe/fork

Push your changes up to your fork and create a Pull Request to the main
project repository.

Thank you again!

.. _tox: https://tox.readthedocs.io/en/latest/
