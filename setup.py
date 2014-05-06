from distutils.core import setup

with open('requirements.txt') as file:
    required = file.read().splitlines()

setup(
    name='htpwd',
    version='0.1.0',
    packages=['htpwd'],
    url='https://github.com/gcavalcante8808/htpwd',
    license='License :: OSI Approved :: Apache Software License',
    author='Gabriel Abdalla Cavalcante',
    author_email='gabriel.cavalcante88@gmail.com',
    description="""A web Interface for users change their own passwords on a
    htpasswd file.""",
    install_requires=required,
)
