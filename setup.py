from distutils.core import setup

setup(
    name='Reactor',
    version='0.1dev',
    author='Juraj Pristach',
    author_email='pristach@gpnet.sk',
    packages=['reactor','reactor.adapters', 'reactor.components', 'reactor.managers','reactor.messages','reactor.models', 'reactor.test', 'plugins'],
    scripts=['bin/reactor.py'],
    url='',
    license='LICENSE.txt',
    description='Home Automation.',
    long_description=open('README.txt').read(),
    install_requires=[
        "pyzmq >= 13.1.0",
        "sqlalchemy >= 7.0.0",
    ],
)